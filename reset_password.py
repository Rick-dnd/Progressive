from models import db, User
from simple_app import app

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('Elegant2000?')
        db.session.commit()
        print('Passwort erfolgreich auf "Elegant2000?" aktualisiert!')
    else:
        print('Admin-Benutzer nicht gefunden!') 