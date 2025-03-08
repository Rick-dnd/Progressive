from datetime import datetime
from . import db

class Project(db.Model):
    """Modell für die Projekte des Progressive Ladies Club"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))  # Kategorie des Projekts (bildung, hilfe, spenden, usw.)
    icon = db.Column(db.String(50))  # Entweder ein Icon-Name oder ein Bildpfad
    color = db.Column(db.String(50))  # CSS-Gradient oder Farbcode
    details = db.Column(db.Text)  # Kann als JSON gespeichert werden für flexible Strukturen
    start_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=999)  # Position für die manuelle Sortierung, Standard ist 999 (niedriger = höhere Priorität)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def to_dict(self):
        """Konvertiert das Projekt in ein Dictionary für JSON-Responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'color': self.color,
            'details': self.details,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'is_current': self.is_current,
            'position': self.position,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 