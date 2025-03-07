from datetime import datetime
from . import db

class News(db.Model):
    """Modell für Neuigkeiten und Updates des Progressive Ladies Club"""
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(100))  # Pfad zum Bild
    is_featured = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<News {self.title}>'
    
    def to_dict(self):
        """Konvertiert die News in ein Dictionary für JSON-Responses"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            'image': self.image,
            'is_featured': self.is_featured,
            'is_published': self.is_published,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 