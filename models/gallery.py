from datetime import datetime
from . import db

class Gallery(db.Model):
    """Modell für Galerie-Elemente des Progressive Ladies Club"""
    __tablename__ = 'gallery'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(100), nullable=False)  # Pfad zum Bild
    thumbnail = db.Column(db.String(100))  # Pfad zum Thumbnail
    order = db.Column(db.Integer, default=0)  # Reihenfolge für die Anzeige
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Gallery {self.title}>'
    
    def to_dict(self):
        """Konvertiert das Galerie-Element in ein Dictionary für JSON-Responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'thumbnail': self.thumbnail,
            'order': self.order,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 