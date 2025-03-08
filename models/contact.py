from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from . import db

class ContactForm(FlaskForm):
    """Formular für Kontaktanfragen"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=100)])
    subject = StringField('Betreff', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Nachricht', validators=[DataRequired(), Length(min=10, max=1000)])

class Contact(db.Model):
    """Modell für Kontaktanfragen des Progressive Ladies Club"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    newsletter = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='neu')  # neu, in_bearbeitung, abgeschlossen
    notes = db.Column(db.Text)  # Interne Notizen
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.email}>'
    
    def to_dict(self):
        """Konvertiert die Kontaktanfrage in ein Dictionary für JSON-Responses"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'newsletter': self.newsletter,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 