from models import db, User
from simple_app import app

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('admin')
        db.session.commit()
        print('Passwort erfolgreich auf "admin" aktualisiert!')
    else:
        print('Admin-Benutzer nicht gefunden!') 