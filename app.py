import os
from flask import Flask, render_template, request, jsonify, current_app, redirect, url_for, flash, session
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
from flask_caching import Cache
from flask_minify import Minify
from flask_assets import Environment, Bundle
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from models import db, Project, News, Gallery, Contact, ContactForm, User
from config import config

mail = Mail()
cache = Cache()
assets = Environment()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin-Zugriffsdekorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Sie haben keine Berechtigung, auf diesen Bereich zuzugreifen.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Admin-Views mit Authentifizierung
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        flash('Bitte melden Sie sich an, um auf den Admin-Bereich zuzugreifen.', 'warning')
        return redirect(url_for('admin_login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('admin_login'))
        return super(SecureAdminIndexView, self).index()

def create_app(config_name='default'):
    """Flask-Anwendungsfabrik"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Extensions initialisieren
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    assets.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'
    login_manager.login_message = 'Bitte melden Sie sich an, um auf diesen Bereich zuzugreifen.'
    login_manager.login_message_category = 'warning'
    
    # Assets konfigurieren
    css_bundle = Bundle(
        'css/main.css',
        'css/animations.css',
        filters='cssmin',
        output='gen/packed.css'
    )
    js_bundle = Bundle(
        'js/main.js',
        'js/animations.js',
        'js/forms.js',
        filters='jsmin',
        output='gen/packed.js'
    )
    assets.register('css_all', css_bundle)
    assets.register('js_all', js_bundle)
    
    # Minify für Produktion aktivieren
    if not app.config['DEBUG']:
        Minify(app=app, html=True, js=True, cssless=True)
    
    # Admin-Bereich einrichten
    admin = Admin(app, name='Progressive Ladies Club Admin', template_mode='bootstrap4', 
                  index_view=SecureAdminIndexView(url='/admin-dashboard'))
    admin.add_view(SecureModelView(Project, db.session, name='Projekte'))
    admin.add_view(SecureModelView(News, db.session, name='News'))
    admin.add_view(SecureModelView(Gallery, db.session, name='Galerie'))
    admin.add_view(SecureModelView(Contact, db.session, name='Kontakte'))
    
    # Routes registrieren
    from routes import main_routes, admin_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes)
    
    # Datenbankinitialisierung
    with app.app_context():
        db.create_all()
        # Admin-Benutzer erstellen, falls keiner existiert
        if not User.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
            admin_user = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(debug=app.config['DEBUG']) 