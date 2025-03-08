from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session, g, make_response
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import os
import json
from sqlalchemy import text
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
import re
from html import escape

from models import db, Project, News, Gallery, Contact, ContactForm, User

app = Flask(__name__)

# Konfiguration
app.config['SECRET_KEY'] = 'progressive-ladies-club-munich-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///progressive_ladies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Admin-Konfiguration
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = 'admin'
app.config['ADMIN_EMAIL'] = 'buchneresther08@gmail.com'

# Mail-Konfiguration (für Produktion anpassen)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'buchneresther08@gmail.com'
app.config['MAIL_PASSWORD'] = 'ihrpassword'  # In Produktion als Umgebungsvariable speichern!
app.config['MAIL_DEFAULT_SENDER'] = 'buchneresther08@gmail.com'

# Zulässige Dateitypen für Bildupload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Funktion zur Überprüfung zulässiger Dateierweiterungen
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Erweiterungen initialisieren
db.init_app(app)

# Login-Manager initialisieren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Bitte melden Sie sich an, um auf diesen Bereich zuzugreifen.'
login_manager.login_message_category = 'warning'

# Add context processor to provide 'now' variable to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Datenbank und Beispieldaten initialisieren
with app.app_context():
    db.create_all()
    
    # Überprüfung der Kategorie und Icons in bestehenden Projekten
    try:
        # Icon-zu-Kategorie-Mapping
        icon_to_category = {
            'fa-graduation-cap': 'bildung',
            'fa-hands-helping': 'hilfe',
            'fa-donate': 'spenden',
            'fa-glass-cheers': 'feiern',
            'fa-leaf': 'natur',
            'fa-users': 'gemeinschaft',
            'fa-theater-masks': 'kultur',
            'fa-running': 'sport',
            'fa-microchip': 'technologie',
            'fa-heartbeat': 'gesundheit',
            'fa-home': 'familie',
            'fa-project-diagram': 'andere'
        }
        
        # Kategorie-zu-Icon-Mapping
        category_to_icon = {
            'bildung': 'fa-graduation-cap',
            'hilfe': 'fa-hands-helping',
            'spenden': 'fa-donate',
            'feiern': 'fa-glass-cheers',
            'natur': 'fa-leaf',
            'gemeinschaft': 'fa-users',
            'kultur': 'fa-theater-masks',
            'sport': 'fa-running',
            'technologie': 'fa-microchip',
            'gesundheit': 'fa-heartbeat',
            'familie': 'fa-home',
            'andere': 'fa-project-diagram'
        }
        
        # Überprüfe, ob die Projekte die richtigen Icons haben
        projects = Project.query.all()
        for project in projects:
            if hasattr(project, 'category') and project.category:
                # Wenn eine Kategorie vorhanden ist, stelle sicher, dass das Icon stimmt
                correct_icon = category_to_icon.get(project.category)
                if correct_icon and project.icon != correct_icon:
                    print(f"Korrigiere Icon für Projekt '{project.title}': von {project.icon} zu {correct_icon}")
                    project.icon = correct_icon
                    db.session.commit()
            elif project.icon:
                # Wenn keine Kategorie vorhanden ist, aber ein Icon, setze die Kategorie
                category = icon_to_category.get(project.icon)
                if category and hasattr(project, 'category'):
                    print(f"Setze Kategorie für Projekt '{project.title}': zu {category}")
                    project.category = category
                    db.session.commit()
            
            # Überprüfe auch die Position und setze sie, falls nicht vorhanden
            if not hasattr(project, 'position') or project.position is None:
                # Setze die Position basierend auf bestehender Sortierung: Zuerst aktuelle, dann nach Datum, dann nach ID
                base_position = 0 if project.is_current else 1000  # Aktuelle Projekte priorisieren
                # Füge noch eine Komponente basierend auf dem Startdatum hinzu (neuere zuerst)
                if project.start_date:
                    days_since_epoch = (project.start_date - datetime(1970, 1, 1).date()).days
                    date_component = 10000 - days_since_epoch  # Umkehren, damit neuere Projekte niedrigere Werte haben
                else:
                    date_component = 5000  # Mittlerer Wert für Projekte ohne Startdatum
                
                # Verwende Index im Array als zusätzliche Komponente für stabile Sortierung
                project.position = base_position + date_component
                print(f"Setze Position für Projekt '{project.title}' auf {project.position}")
                db.session.commit()
            
            print(f"Projekt '{project.title}': Kategorie={getattr(project, 'category', 'N/A')}, Icon={project.icon}, Position={getattr(project, 'position', 'N/A')}")
    except Exception as e:
        print(f"Warnung: Überprüfung der Projektdaten fehlgeschlagen: {e}")
        # Wir lassen den Fehler durch, damit die App trotzdem startet
    
    # Erstelle einen Standard-Admin-Benutzer, wenn keiner existiert
    if User.query.count() == 0:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('start123')
        db.session.add(admin)
        db.session.commit()
    
    # Beispielprojekte erstellen, falls keine vorhanden sind
    if Project.query.count() == 0:
        sample_projects = [
            {
                'title': 'Bildung für alle',
                'description': 'Förderung von Bildungsmöglichkeiten für benachteiligte junge Frauen in München.',
                'icon': 'fas fa-graduation-cap',
                'color': 'bg-gradient-to-r from-purple-600 to-pink-500',
                'details': '''
                    Unser Flaggschiff-Projekt "Bildung für alle" zielt darauf ab, jungen Frauen aus benachteiligten Verhältnissen Zugang zu hochwertiger Bildung zu ermöglichen. 
                    Durch Stipendien, Mentoring-Programme und Lernressourcen schaffen wir Chancengleichheit und fördern die persönliche und berufliche Entwicklung.
                    
                    Das Projekt umfasst Workshops zu digitalen Fähigkeiten, Sprachkurse und Berufsberatung, um die Teilnehmerinnen auf die Anforderungen des modernen Arbeitsmarktes vorzubereiten.
                ''',
                'start_date': date(2022, 3, 15),
                'is_current': True
            },
            {
                'title': 'Umweltschutz Initiative',
                'description': 'Gemeinschaftliche Aktionen für mehr Nachhaltigkeit und Umweltbewusstsein in unserer Stadt.',
                'icon': 'fas fa-leaf',
                'color': 'bg-gradient-to-r from-green-500 to-teal-400',
                'details': '''
                    Die "Umweltschutz Initiative" vereint Frauen, die sich für den Schutz unserer Umwelt einsetzen. Wir organisieren regelmäßige Reinigungsaktionen in Parks und Grünflächen, 
                    pflanzen Bäume und setzen uns für nachhaltige Praktiken in unserer Gemeinschaft ein.
                    
                    Durch Bildungsveranstaltungen sensibilisieren wir für Umweltthemen und fördern nachhaltiges Handeln im Alltag. Unsere Workshops zu Themen wie Upcycling, 
                    Abfallvermeidung und nachhaltigem Konsum tragen zu einem bewussteren Umgang mit Ressourcen bei.
                ''',
                'start_date': date(2023, 5, 10),
                'is_current': True
            }
        ]
        
        for project_data in sample_projects:
            project = Project(
                title=project_data['title'],
                description=project_data['description'],
                icon=project_data['icon'],
                color=project_data['color'],
                details=project_data['details'],
                start_date=project_data['start_date'],
                is_current=project_data['is_current']
            )
            db.session.add(project)
        
        db.session.commit()
    
    # Beispiel-News erstellen, falls keine vorhanden sind
    if News.query.count() == 0:
        sample_news = [
            {
                'title': 'Erfolgreicher Abschluss des Mentoring-Programms',
                'content': 'Unser diesjähriges Mentoring-Programm wurde erfolgreich abgeschlossen. 15 Teilnehmerinnen haben das Programm durchlaufen und wertvolle Erfahrungen gesammelt. Die Abschlussveranstaltung fand im Kulturzentrum München statt.',
                'date': datetime.now() - timedelta(days=10),
                'image': 'img/news/c079074a1858489bbda784035275db06_51579ab90620cb36fb8592b19cd4280f.jpg',
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Neue Workshops im Herbst',
                'content': 'Ab September starten wir mit neuen Workshop-Reihen zu den Themen "Digitale Kompetenz", "Finanzen für Frauen" und "Nachhaltigkeit im Alltag". Die Anmeldung ist ab sofort möglich.',
                'date': datetime.now() - timedelta(days=5),
                'image': 'img/news/27161cea4726474691cb0a9c55e766bd_vRj1qBcrHdFs1CwY-generated_image.jpg',
                'is_featured': True,
                'is_published': True
            }
        ]
        
        for news_data in sample_news:
            news = News(
                title=news_data['title'],
                content=news_data['content'],
                date=news_data['date'],
                image=news_data['image'],
                is_featured=news_data['is_featured'],
                is_published=news_data['is_published']
            )
            db.session.add(news)
        
        db.session.commit()
    
    # Beispiel-Galerie erstellen, falls keine vorhanden ist
    if Gallery.query.count() == 0:
        sample_gallery = [
            {
                'title': 'Sommerfest 2023',
                'description': 'Eindrücke von unserem jährlichen Sommerfest im Englischen Garten.',
                'image': 'img/gallery/57516be4efef49b6abda73349cd5ffc4_wallpaperflare.com_wallpaper_1.jpg',
                'thumbnail': 'img/gallery/57516be4efef49b6abda73349cd5ffc4_wallpaperflare.com_wallpaper_1.jpg',
                'order': 1,
                'is_active': True
            },
            {
                'title': 'Workshop-Reihe "Starke Frauen"',
                'description': 'Impressionen aus unserer Workshop-Reihe zum Thema Selbstbewusstsein und Führung.',
                'image': 'img/gallery/624c37d04b0c45a7be09a3b42c3f9550_wallpaperflare.com_wallpaper_1.jpg',
                'thumbnail': 'img/gallery/624c37d04b0c45a7be09a3b42c3f9550_wallpaperflare.com_wallpaper_1.jpg',
                'order': 2,
                'is_active': True
            }
        ]
        
        for gallery_data in sample_gallery:
            gallery = Gallery(
                title=gallery_data['title'],
                description=gallery_data['description'],
                image=gallery_data['image'],
                thumbnail=gallery_data['thumbnail'],
                order=gallery_data['order'],
                is_active=gallery_data['is_active']
            )
            db.session.add(gallery)
        
        db.session.commit()

# Hauptseite
@app.route('/')
def index():
    # Verbesserte Sortierung: Erst nach Position (höhere Werte zuerst), dann aktuelle Projekte, dann nach Startdatum, dann nach ID
    projects = Project.query.order_by(Project.position.desc(), Project.is_current.desc(), Project.start_date.desc(), Project.id.asc()).all()
    
    # DEBUG: Alle Projekte anzeigen
    print("\n=== DEBUG: PROJEKTE FÜR FRONTEND ===")
    print(f"Anzahl der Projekte: {len(projects)}")
    for idx, project in enumerate(projects):
        print(f"Projekt {idx+1}: ID={project.id}, Titel='{project.title}', is_current={project.is_current}, Position={project.position}")
    print("=====================================\n")
    
    # News paginieren
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Anzahl der News pro Seite
    news_items_query = News.query.filter_by(is_published=True).order_by(News.date.desc())
    total_news = news_items_query.count()
    news_items = news_items_query.limit(per_page).all()
    has_more_news = total_news > per_page
    
    # Galerie
    gallery_items = Gallery.query.order_by(Gallery.created_at.desc()).all()
    
    # Debug-Ausgabe der Galerie-Einträge
    print("GALERIE-EINTRÄGE:")
    for item in gallery_items:
        print(f"ID: {item.id}, Titel: {item.title}, Bild: {item.image}")
    
    contact_form = ContactForm()
    
    return render_template('index.html', 
                          projects=projects, 
                          news_items=news_items, 
                          gallery_items=gallery_items,
                          current_page=1,  # Erste Seite
                          has_more_news=has_more_news,
                          total_news=total_news,
                          contact_form=contact_form)

# Impressum und Datenschutz
@app.route('/imprint')
def imprint():
    return render_template('legal/imprint.html')

# News-Detailansicht
@app.route('/news/<int:id>')
def news_detail(id):
    news_item = News.query.get_or_404(id)
    return render_template('news/detail.html', news_item=news_item)

@app.route('/privacy')
def privacy():
    return render_template('legal/privacy.html')

# Admin-Bereich
@app.route('/admin')
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = 'remember' in request.form
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.verify_password(password):
        login_user(user, remember=remember)
        
        # Letztes Login-Datum aktualisieren
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        flash('You have been successfully logged in.', 'success')
        
        # Weiterleitung zur Zielseite oder zum Dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        else:
            return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this area.', 'danger')
        return redirect(url_for('index'))
    
    project_count = Project.query.count()
    news_count = News.query.count()
    gallery_count = Gallery.query.count()
    contact_count = Contact.query.count()
    
    return render_template('admin/dashboard.html', 
                          project_count=project_count,
                          news_count=news_count,
                          gallery_count=gallery_count,
                          contact_count=contact_count)

# API-Endpunkte
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Neue Kontaktanfrage speichern
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            newsletter=form.newsletter.data
        )
        db.session.add(contact)
        db.session.commit()
        
        # Hier würde die E-Mail-Versendung stattfinden
        # In der einfachen App simulieren wir nur den Erfolg
        
        return jsonify({'success': True, 'message': 'Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden.'}), 200
    
    return jsonify({'success': False, 'errors': form.errors}), 400

@app.route('/api/load-more-news')
def load_more_news():
    """AJAX-Route zum Laden weiterer News-Einträge"""
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Anzahl der News pro Seite
    
    # News für die angeforderte Seite laden (3 Einträge pro Seite)
    news_items = News.query.filter_by(is_published=True).order_by(News.date.desc()).offset((page-1) * per_page).limit(per_page).all()
    
    # Gesamtanzahl der News zur Berechnung der verbleibenden Einträge
    total_news = News.query.filter_by(is_published=True).count()
    
    # Prüfen, ob es weitere News gibt
    has_more = total_news > (page * per_page)
    
    # HTML für die neuen News-Einträge generieren
    html = ''
    for news_item in news_items:
        # Inhaltstext für die Prüfung vorbereiten
        content_text = news_item.content
        if content_text:
            # HTML-Tags entfernen
            content_text = re.sub(r'<[^>]+>', '', content_text)
        else:
            content_text = ''
            
        # Gekürzten Text erzeugen
        truncated_content = content_text[:150] + ('...' if len(content_text) > 150 else '')
        show_read_more = len(content_text) > 150
        
        # HTML für den News-Eintrag
        news_html = f'''
        <div class="bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
            {'<div class="h-52 overflow-hidden"><img src="' + url_for('static', filename=news_item.image) + '" alt="' + news_item.title + '" class="w-full h-full object-cover transform hover:scale-105 transition-transform duration-300"></div>' if news_item.image else '<div class="h-52 bg-gradient-to-r from-primary to-secondary flex items-center justify-center"><i class="fas fa-newspaper text-white text-5xl"></i></div>'}
            <div class="p-6">
                <div class="text-sm text-gray-500 mb-2">{news_item.date.strftime('%d.%m.%Y') if news_item.date else ''}</div>
                <h3 class="text-xl font-bold mb-2">{escape(news_item.title)}</h3>
                <div class="text-gray-600 mb-4 line-clamp-3">{escape(truncated_content)}</div>
                {('<a href="#" class="text-primary hover:text-secondary transition-colors duration-200 inline-flex items-center"><span class="mr-1">Weiterlesen</span><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg></a>') if show_read_more else ''}
            </div>
        </div>
        '''
        html += news_html
        
    return jsonify({
        'html': html,
        'has_more': has_more,
        'next_page': page + 1 if has_more else page
    })

# Fehlerbehandlung
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Projektverwaltung
@app.route('/admin/projects')
@login_required
def project_index():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    projects = Project.query.order_by(Project.position.desc(), Project.is_current.desc(), Project.start_date.desc()).all()
    return render_template('admin/projects/index.html', projects=projects)

@app.route('/admin/projects/create', methods=['GET', 'POST'])
@login_required
def project_create():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        details = request.form.get('details')
        category = request.form.get('category')
        
        # Automatisch das richtige Icon basierend auf der Kategorie setzen
        icon_map = {
            'bildung': 'fa-graduation-cap',
            'hilfe': 'fa-hands-helping',
            'spenden': 'fa-donate',
            'feiern': 'fa-glass-cheers',
            'natur': 'fa-leaf',
            'gemeinschaft': 'fa-users',
            'kultur': 'fa-theater-masks',
            'sport': 'fa-running',
            'technologie': 'fa-microchip',
            'gesundheit': 'fa-heartbeat',
            'familie': 'fa-home',
            'andere': 'fa-project-diagram'
        }
        
        # Icon automatisch basierend auf der Kategorie setzen
        icon = icon_map.get(category, 'fa-project-diagram')
        
        color = request.form.get('color')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        is_current = 'is_current' in request.form
        # Behandeln Sie leere Werte und stellen Sie sicher, dass position ein gültiger Integer-Wert ist
        try:
            position = int(request.form.get('position', 999))
        except (ValueError, TypeError):
            position = 999  # Standardwert, wenn keine gültige Zahl angegeben wird
        
        project = Project(
            title=title,
            description=description,
            details=details,
            category=category,
            icon=icon,
            color=color,
            start_date=start_date,
            is_current=is_current,
            position=position
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Projekt wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('project_index'))
    
    return render_template('admin/projects/create.html')

@app.route('/admin/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.details = request.form.get('details')
        project.category = request.form.get('category')
        
        # Automatisch das richtige Icon basierend auf der Kategorie setzen
        icon_map = {
            'bildung': 'fa-graduation-cap',
            'hilfe': 'fa-hands-helping',
            'spenden': 'fa-donate',
            'feiern': 'fa-glass-cheers',
            'natur': 'fa-leaf',
            'gemeinschaft': 'fa-users',
            'kultur': 'fa-theater-masks',
            'sport': 'fa-running',
            'technologie': 'fa-microchip',
            'gesundheit': 'fa-heartbeat',
            'familie': 'fa-home',
            'andere': 'fa-project-diagram'
        }
        
        # Icon automatisch basierend auf der Kategorie setzen
        project.icon = icon_map.get(project.category, 'fa-project-diagram')
        
        project.color = request.form.get('color')
        project.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        project.is_current = 'is_current' in request.form
        # Behandeln Sie leere Werte und stellen Sie sicher, dass position ein gültiger Integer-Wert ist
        try:
            project.position = int(request.form.get('position', 999))
        except (ValueError, TypeError):
            project.position = 999  # Standardwert, wenn keine gültige Zahl angegeben wird
        project.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Projekt wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('project_index'))
    
    return render_template('admin/projects/edit.html', project=project)

@app.route('/admin/projects/<int:id>/delete', methods=['POST'])
@login_required
def project_delete(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    project = Project.query.get_or_404(id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        
        flash('Projekt wurde erfolgreich gelöscht.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen des Projekts: {str(e)}', 'danger')
    
    return redirect(url_for('project_index'))

# News-Verwaltung
@app.route('/admin/news')
@login_required
def news_index():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    news_items = News.query.order_by(News.date.desc()).all()
    return render_template('admin/news/index.html', news_items=news_items)

@app.route('/admin/news/create', methods=['GET', 'POST'])
@login_required
def news_create():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        is_featured = 'is_featured' in request.form
        is_published = 'is_published' in request.form
        
        # Standardwert für das Bild
        image_path = ''
        
        # Bildupload verarbeiten
        if 'image_file' in request.files and request.files['image_file'].filename:
            try:
                image_file = request.files['image_file']
                filename = secure_filename(image_file.filename)
                # Eindeutigen Dateinamen erstellen
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                # Relativer Pfad zum static-Verzeichnis
                file_path = f'img/news/{unique_filename}'
                
                # Bild mit Pillow öffnen und verarbeiten
                img = Image.open(image_file)
                
                # Optimieren für Cards mit 3:2 Verhältnis (passend zu h-52)
                target_ratio = 3/2  # Seitenverhältnis für News-Cards
                
                # Aktuelle Dimensionen und Verhältnis
                width, height = img.size
                img_ratio = width / height
                
                # Für optimale Anzeige mit object-cover:
                # Wir schneiden das Bild zentral zu, damit es dem Zielverhältnis entspricht
                if abs(img_ratio - target_ratio) > 0.01:  # Wenn Verhältnis abweicht
                    if img_ratio > target_ratio:
                        # Bild ist zu breit, wir schneiden an den Seiten
                        new_width = int(height * target_ratio)
                        left = (width - new_width) // 2
                        img = img.crop((left, 0, left + new_width, height))
                    else:
                        # Bild ist zu hoch, wir schneiden oben und unten
                        new_height = int(width / target_ratio)
                        top = (height - new_height) // 2
                        img = img.crop((0, top, width, top + new_height))
                
                # Speichergröße optimieren
                target_size = (1200, 800)  # Zielgröße, behält 3:2 Verhältnis bei
                img.thumbnail(target_size, Image.LANCZOS)
                
                # Absoluten Pfad für das Speichern erstellen
                abs_path = os.path.join(app.root_path, 'static', file_path)
                
                # Sicherstellen, dass das Verzeichnis existiert
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                
                # Bild mit optimierter Qualität speichern
                img.save(abs_path, quality=90, optimize=True)
                
                # Pfad für die Datenbank speichern
                image_path = file_path
                print(f"Bild erfolgreich gespeichert unter: {abs_path}")
            except Exception as e:
                flash(f'Fehler beim Hochladen des Bildes: {str(e)}', 'danger')
                print(f"Fehler beim Bildupload: {str(e)}")
        
        news = News(
            title=title,
            content=content,
            date=datetime.utcnow(),
            image=image_path,
            is_featured=is_featured,
            is_published=is_published
        )
        
        db.session.add(news)
        db.session.commit()
        
        flash('News-Eintrag wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('news_index'))
    
    return render_template('admin/news/create.html')

@app.route('/admin/news/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def news_edit(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    news = News.query.get_or_404(id)
    
    if request.method == 'POST':
        news.title = request.form.get('title')
        news.content = request.form.get('content')
        news.is_featured = 'is_featured' in request.form
        news.is_published = 'is_published' in request.form
        news.updated_at = datetime.utcnow()
        
        # Bildupload verarbeiten
        if 'image_file' in request.files and request.files['image_file'].filename:
            try:
                image_file = request.files['image_file']
                filename = secure_filename(image_file.filename)
                # Eindeutigen Dateinamen erstellen
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                # Relativer Pfad zum static-Verzeichnis
                file_path = f'img/news/{unique_filename}'
                
                # Bild mit Pillow öffnen und verarbeiten
                img = Image.open(image_file)
                
                # Optimieren für Cards mit 3:2 Verhältnis (passend zu h-52)
                target_ratio = 3/2  # Seitenverhältnis für News-Cards
                
                # Aktuelle Dimensionen und Verhältnis
                width, height = img.size
                img_ratio = width / height
                
                # Für optimale Anzeige mit object-cover:
                # Wir schneiden das Bild zentral zu, damit es dem Zielverhältnis entspricht
                if abs(img_ratio - target_ratio) > 0.01:  # Wenn Verhältnis abweicht
                    if img_ratio > target_ratio:
                        # Bild ist zu breit, wir schneiden an den Seiten
                        new_width = int(height * target_ratio)
                        left = (width - new_width) // 2
                        img = img.crop((left, 0, left + new_width, height))
                    else:
                        # Bild ist zu hoch, wir schneiden oben und unten
                        new_height = int(width / target_ratio)
                        top = (height - new_height) // 2
                        img = img.crop((0, top, width, top + new_height))
                
                # Speichergröße optimieren
                target_size = (1200, 800)  # Zielgröße, behält 3:2 Verhältnis bei
                img.thumbnail(target_size, Image.LANCZOS)
                
                # Absoluten Pfad für das Speichern erstellen
                abs_path = os.path.join(app.root_path, 'static', file_path)
                
                # Sicherstellen, dass das Verzeichnis existiert
                os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                
                # Bild mit optimierter Qualität speichern
                img.save(abs_path, quality=90, optimize=True)
                
                # Altes Bild löschen, wenn vorhanden
                if news.image and os.path.exists(os.path.join(app.root_path, 'static', news.image)):
                    try:
                        os.remove(os.path.join(app.root_path, 'static', news.image))
                    except Exception as e:
                        print(f"Fehler beim Löschen des alten Bildes: {str(e)}")
                
                # Pfad für die Datenbank speichern
                news.image = file_path
                print(f"Bild erfolgreich aktualisiert und gespeichert unter: {abs_path}")
            except Exception as e:
                flash(f'Fehler beim Hochladen des Bildes: {str(e)}', 'danger')
                print(f"Fehler beim Bildupload: {str(e)}")
        
        db.session.commit()
        
        flash('News-Eintrag wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('news_index'))
    
    return render_template('admin/news/edit.html', news=news)

@app.route('/admin/news/<int:id>/delete', methods=['POST'])
@login_required
def news_delete(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    news = News.query.get_or_404(id)
    
    db.session.delete(news)
    db.session.commit()
    
    flash('News-Eintrag wurde erfolgreich gelöscht.', 'success')
    return redirect(url_for('news_index'))

# Galerie-Verwaltung
@app.route('/admin/gallery')
@login_required
def gallery_index():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    gallery_items = Gallery.query.order_by(Gallery.order.asc()).all()
    return render_template('admin/gallery/index.html', gallery_items=gallery_items)

@app.route('/admin/gallery/create', methods=['GET', 'POST'])
@login_required
def gallery_create():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        order = request.form.get('order', 0)
        is_active = 'is_active' in request.form
        
        # Bildverarbeitung
        image_path = None
        thumbnail_path = None
        
        if 'image_file' in request.files and request.files['image_file'].filename:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename):
                # Eindeutigen Dateinamen erstellen
                filename = secure_filename(image_file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Pfade erstellen
                img_dir = os.path.join(app.static_folder, 'img', 'gallery')
                os.makedirs(img_dir, exist_ok=True)
                
                # Pfade für die Datenbank mit Vorwärtsschrägstrichen (/)
                image_path = f"img/gallery/{unique_filename}"
                
                # Vollständiger Pfad für das Speichern der Datei
                full_path = os.path.join(app.static_folder, 'img', 'gallery', unique_filename)
                
                # Bild speichern
                image_file.save(full_path)
                print(f"Bild erfolgreich gespeichert unter: {os.path.abspath(full_path)}")
        
        # Thumbnail-Verarbeitung
        if 'thumbnail_file' in request.files and request.files['thumbnail_file'].filename:
            thumbnail_file = request.files['thumbnail_file']
            if thumbnail_file and allowed_file(thumbnail_file.filename):
                # Eindeutigen Dateinamen erstellen
                filename = secure_filename(thumbnail_file.filename)
                unique_filename = f"thumb_{uuid.uuid4().hex}_{filename}"
                
                # Pfade erstellen
                img_dir = os.path.join(app.static_folder, 'img', 'gallery')
                os.makedirs(img_dir, exist_ok=True)
                
                # Pfade für die Datenbank mit Vorwärtsschrägstrichen (/)
                thumbnail_path = f"img/gallery/{unique_filename}"
                
                # Vollständiger Pfad für das Speichern der Datei
                full_path = os.path.join(app.static_folder, 'img', 'gallery', unique_filename)
                
                # Thumbnail speichern
                thumbnail_file.save(full_path)
        
        gallery = Gallery(
            title=title,
            description=description,
            image=image_path,
            thumbnail=thumbnail_path or image_path,  # Wenn kein Thumbnail, verwende das Hauptbild
            order=order,
            is_active=is_active
        )
        
        db.session.add(gallery)
        db.session.commit()
        
        flash('Galerie-Eintrag wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('gallery_index'))
    
    return render_template('admin/gallery/create.html')

@app.route('/admin/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def gallery_edit(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    gallery = Gallery.query.get_or_404(id)
    
    if request.method == 'POST':
        gallery.title = request.form.get('title')
        gallery.description = request.form.get('description', '')
        gallery.order = request.form.get('order', 0)
        gallery.is_active = 'is_active' in request.form
        
        # Bildverarbeitung
        if 'image_file' in request.files and request.files['image_file'].filename:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename):
                # Altes Bild löschen, wenn vorhanden
                if gallery.image and gallery.image.startswith('img/gallery/'):
                    old_file = os.path.join(app.static_folder, gallery.image.replace('/', os.path.sep))
                    try:
                        if os.path.exists(old_file):
                            os.remove(old_file)
                    except Exception as e:
                        print(f"Fehler beim Löschen der alten Datei: {e}")
                
                # Eindeutigen Dateinamen erstellen
                filename = secure_filename(image_file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Pfade erstellen
                img_dir = os.path.join(app.static_folder, 'img', 'gallery')
                os.makedirs(img_dir, exist_ok=True)
                
                # Pfade für die Datenbank mit Vorwärtsschrägstrichen (/)
                image_path = f"img/gallery/{unique_filename}"
                
                # Vollständiger Pfad für das Speichern der Datei
                full_path = os.path.join(app.static_folder, 'img', 'gallery', unique_filename)
                
                # Bild speichern
                image_file.save(full_path)
                print(f"Bild erfolgreich gespeichert unter: {os.path.abspath(full_path)}")
                
                # Pfad in der Datenbank aktualisieren
                gallery.image = image_path
        
        # Thumbnail-Verarbeitung
        if 'thumbnail_file' in request.files and request.files['thumbnail_file'].filename:
            thumbnail_file = request.files['thumbnail_file']
            if thumbnail_file and allowed_file(thumbnail_file.filename):
                # Altes Thumbnail löschen, wenn vorhanden
                if gallery.thumbnail and gallery.thumbnail != gallery.image and gallery.thumbnail.startswith('img/gallery/'):
                    old_file = os.path.join(app.static_folder, gallery.thumbnail.replace('/', os.path.sep))
                    try:
                        if os.path.exists(old_file):
                            os.remove(old_file)
                    except Exception as e:
                        print(f"Fehler beim Löschen des alten Thumbnails: {e}")
                
                # Eindeutigen Dateinamen erstellen
                filename = secure_filename(thumbnail_file.filename)
                unique_filename = f"thumb_{uuid.uuid4().hex}_{filename}"
                
                # Pfade erstellen
                img_dir = os.path.join(app.static_folder, 'img', 'gallery')
                os.makedirs(img_dir, exist_ok=True)
                
                # Pfade für die Datenbank mit Vorwärtsschrägstrichen (/)
                thumbnail_path = f"img/gallery/{unique_filename}"
                
                # Vollständiger Pfad für das Speichern der Datei
                full_path = os.path.join(app.static_folder, 'img', 'gallery', unique_filename)
                
                # Thumbnail speichern
                thumbnail_file.save(full_path)
                
                # Pfad in der Datenbank aktualisieren
                gallery.thumbnail = thumbnail_path
        
        db.session.commit()
        flash('Galerie-Eintrag wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('gallery_index'))
    
    return render_template('admin/gallery/edit.html', gallery=gallery)

@app.route('/admin/gallery/<int:id>/delete', methods=['POST'])
@login_required
def gallery_delete(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    gallery = Gallery.query.get_or_404(id)
    
    db.session.delete(gallery)
    db.session.commit()
    
    flash('Galerie-Eintrag wurde erfolgreich gelöscht.', 'success')
    return redirect(url_for('gallery_index'))

# Kontaktverwaltung
@app.route('/admin/contacts')
@login_required
def contact_index():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts/index.html', contacts=contacts)

@app.route('/admin/contacts/<int:id>/view')
@login_required
def contact_view(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    contact = Contact.query.get_or_404(id)
    return render_template('admin/contacts/view.html', contact=contact)

@app.route('/admin/contacts/<int:id>/update-status', methods=['POST'])
@login_required
def contact_update_status(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    contact = Contact.query.get_or_404(id)
    
    status = request.form.get('status')
    notes = request.form.get('notes', contact.notes)
    
    if status in ['neu', 'in_bearbeitung', 'abgeschlossen']:
        contact.status = status
        contact.notes = notes
        contact.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Status wurde erfolgreich aktualisiert.', 'success')
    else:
        flash('Ungültiger Status.', 'danger')
    
    return redirect(url_for('contact_view', id=id))

@app.route('/admin/contacts/<int:id>/delete', methods=['POST'])
@login_required
def contact_delete(id):
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    contact = Contact.query.get_or_404(id)
    
    db.session.delete(contact)
    db.session.commit()
    
    flash('Kontaktanfrage wurde erfolgreich gelöscht.', 'success')
    return redirect(url_for('contact_index'))

# Route zum Zurücksetzen der Autoinkrement-Sequenz für die Projekte-Tabelle
@app.route('/admin/reset-project-sequence', methods=['POST'])
@login_required
def reset_project_sequence():
    if not current_user.is_admin:
        flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
        return redirect(url_for('index'))
    
    try:
        # SQLite-spezifisches Command zum Zurücksetzen der Sequenz
        max_id = db.session.execute(text('SELECT MAX(id) FROM projects')).scalar() or 0
        db.session.execute(text('DELETE FROM sqlite_sequence WHERE name = "projects"'))
        db.session.execute(text('INSERT INTO sqlite_sequence (name, seq) VALUES ("projects", :max_id)'), {'max_id': max_id})
        db.session.commit()
        flash('Die Projekt-ID-Sequenz wurde erfolgreich zurückgesetzt.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Zurücksetzen der Sequenz: {str(e)}', 'danger')
    
    return redirect(url_for('project_index'))

@app.before_request
def handle_language():
    """Verarbeitet die Spracheinstellungen des Benutzers."""
    # Standard ist Englisch
    g.lang = 'en'
    
    # Prüfe, ob ein Sprachparameter in der URL ist
    lang = request.args.get('lang')
    if lang in ['de', 'en']:
        g.lang = lang
        session['lang'] = lang
    elif 'lang' in session:
        g.lang = session.get('lang')
    
    # Pfad mit /de/ beginnt
    if request.path.startswith('/de/'):
        g.lang = 'de'
        session['lang'] = 'de'

@app.route('/robots.txt')
def robots_txt():
    """Generiert eine robots.txt Datei für SEO."""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: https://www.elegantprogressiveladies.org/sitemap.xml
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == '__main__':
    app.run(debug=True) 