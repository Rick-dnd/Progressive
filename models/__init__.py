from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .project import Project
from .news import News
from .gallery import Gallery
from .contact import Contact, ContactForm
from .user import User

__all__ = [
    'db', 
    'Project', 
    'News', 
    'Gallery', 
    'Contact', 
    'ContactForm',
    'User'
] 