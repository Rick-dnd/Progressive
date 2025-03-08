from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash
from models import db, Project, News, Gallery, Contact, ContactForm, User
from flask_mail import Mail, Message

# Blueprints erstellen
main_routes = Blueprint('main', __name__)
admin_routes = Blueprint('admin', __name__, url_prefix='/admin')

# E-Mail-Instanz
mail = Mail()

# Cache-Instanz aus der Hauptapp
from app import cache

# Admin-Zugriffsdekorator (zusätzlich zum Blueprint)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Kontext-Prozessor für globale Variablen
@main_routes.context_processor
def inject_globals():
    """Globale Variablen für Templates injizieren"""
    return dict(
        current_projects=Project.query.filter_by(is_current=True).all(),
        featured_news=News.query.filter_by(is_featured=True).order_by(News.date.desc()).limit(3).all()
    )

# Haupt-Routen
@main_routes.route('/')
@cache.cached(timeout=60)
def index():
    """Hauptseite der One-Page-Website"""
    # Verbesserte Sortierung: Erst aktuelle Projekte, dann nach Startdatum, dann nach ID (neuer zuerst)
    projects = Project.query.order_by(Project.is_current.desc(), Project.start_date.desc(), Project.id.desc()).all()
    news_items = News.query.filter_by(is_published=True).order_by(News.date.desc()).limit(6).all()
    gallery_items = Gallery.query.filter_by(is_active=True).order_by(Gallery.order.asc()).all()
    contact_form = ContactForm()
    
    return render_template('index.html', 
                          projects=projects, 
                          news_items=news_items, 
                          gallery_items=gallery_items, 
                          contact_form=contact_form)

@main_routes.route('/imprint')
def imprint():
    """Impressum-Seite"""
    return render_template('legal/imprint.html')

@main_routes.route('/privacy')
def privacy():
    """Datenschutz-Seite"""
    return render_template('legal/privacy.html')

# API-Routen
@main_routes.route('/api/contact', methods=['POST'])
def handle_contact():
    """API-Endpunkt für Kontaktformular"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Neue Kontaktanfrage speichern
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            newsletter=False  # Setze standardmäßig auf False, da kein Newsletter angeboten wird
        )
        db.session.add(contact)
        db.session.commit()
        
        # E-Mail senden
        msg = Message(
            subject=f'[Progressive Ladies Club] Neue Anfrage: {form.subject.data}',
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
            body=f'Neue Anfrage von {form.name.data} ({form.email.data}):\n\n{form.message.data}',
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        try:
            mail.send(msg)
            # Bestätigungs-Mail an Absender
            confirmation = Message(
                subject='Ihre Anfrage an den Progressive Ladies Club',
                recipients=[form.email.data],
                body=f'Sehr geehrte(r) {form.name.data},\n\nvielen Dank für Ihre Anfrage. Wir werden uns in Kürze bei Ihnen melden.\n\nMit freundlichen Grüßen,\nIhr Progressive Ladies Club Team',
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(confirmation)
            
            return jsonify({'success': True, 'message': 'Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden.'}), 200
        except Exception as e:
            # Bei E-Mail-Fehler trotzdem Erfolg zurückgeben, da Daten gespeichert wurden
            return jsonify({'success': True, 'message': 'Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden.'}), 200
    
    return jsonify({'success': False, 'errors': form.errors}), 400

@main_routes.route('/api/projects')
def get_projects():
    """API-Endpunkt für Projekte"""
    is_current = request.args.get('current', None)
    
    if is_current is not None:
        is_current = is_current.lower() == 'true'
        projects = Project.query.filter_by(is_current=is_current).order_by(Project.start_date.desc(), Project.id.desc()).all()
    else:
        projects = Project.query.order_by(Project.is_current.desc(), Project.start_date.desc(), Project.id.desc()).all()
    
    return jsonify([project.to_dict() for project in projects])

@main_routes.route('/api/news')
def get_news():
    """API-Endpunkt für News"""
    limit = request.args.get('limit', type=int)
    
    query = News.query.filter_by(is_published=True).order_by(News.date.desc())
    
    if limit:
        query = query.limit(limit)
        
    news_items = query.all()
    
    return jsonify([news.to_dict() for news in news_items])

# Admin-Routen
@admin_routes.route('/')
def admin_login():
    """Admin-Login-Seite"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))
    
    return render_template('admin/login.html')

@admin_routes.route('/login', methods=['POST'])
def login():
    """Admin-Login-Verarbeitung"""
    username = request.form.get('username')
    password = request.form.get('password')
    remember = 'remember' in request.form
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.verify_password(password):
        login_user(user, remember=remember)
        
        # Letztes Login-Datum aktualisieren
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        flash('Sie wurden erfolgreich angemeldet.', 'success')
        
        # Weiterleitung zur Zielseite oder zum Dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        else:
            return redirect(url_for('admin.dashboard'))
    else:
        flash('Ungültiger Benutzername oder Passwort.', 'danger')
        return redirect(url_for('admin.admin_login'))

@admin_routes.route('/logout')
@login_required
def logout():
    """Admin-Logout"""
    logout_user()
    flash('Sie wurden erfolgreich abgemeldet.', 'success')
    return redirect(url_for('main.index'))

@admin_routes.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin-Dashboard"""
    project_count = Project.query.count()
    news_count = News.query.count()
    gallery_count = Gallery.query.count()
    contact_count = Contact.query.count()
    
    # Letzten Kontaktanfragen
    latest_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          project_count=project_count,
                          news_count=news_count,
                          gallery_count=gallery_count,
                          contact_count=contact_count,
                          latest_contacts=latest_contacts)

# Error Handler für die Hauptapp
@main_routes.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main_routes.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500 