# Elegant Progressive Ladies Club Munich e.V. - Website

Eine moderne, responsive One-Page-Website für den Elegant Progressive Ladies Club Munich e.V., entwickelt mit Flask, TailwindCSS und Alpine.js.

## Projektübersicht

Diese Website wurde entwickelt, um die Mission, Projekte und Aktivitäten des Progressive Ladies Club zu präsentieren. Die Seite ist als One-Page-Webanwendung konzipiert, die verschiedene Abschnitte wie Über Uns, Projekte, News und Kontakt in einer einzigen, elegant scrollbaren Seite vereint.

## Technologiestack

### Backend
- **Flask**: Python-Webframework für die Anwendungslogik
- **SQLAlchemy**: ORM für Datenbankinteraktionen
- **Flask-WTF**: Für Formularvalidierung und -verarbeitung
- **Flask-Mail**: Für E-Mail-Funktionalität
- **Flask-Admin**: Admin-Bereich für Content-Management
- **Flask-Caching**: Für verbesserte Performance

### Frontend
- **Jinja2**: Template-Engine (in Flask integriert)
- **TailwindCSS**: Utility-first CSS-Framework für responsives Design
- **Alpine.js**: Leichtgewichtiges JavaScript-Framework für UI-Interaktionen
- **ScrollReveal**: Für Scroll-basierte Animationen
- **Font Awesome**: Icon-Bibliothek

## Projektstruktur

```
progressive_ladies_club/
├── app.py                 # Flask-Hauptanwendung
├── config.py              # Konfigurationseinstellungen
├── requirements.txt       # Python-Abhängigkeiten
├── models/                # Datenmodelle
│   ├── __init__.py
│   ├── project.py
│   ├── news.py
│   ├── gallery.py
│   └── contact.py
├── static/                # Statische Dateien
│   ├── css/
│   │   ├── main.css
│   │   └── animations.css
│   ├── js/
│   │   ├── main.js
│   │   ├── animations.js
│   │   └── forms.js
│   └── images/
├── templates/             # HTML-Templates
│   ├── base.html
│   ├── index.html
│   ├── components/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── project_card.html
│   │   └── contact_form.html
│   └── legal/
│       ├── imprint.html
│       └── privacy.html
```

## Hauptmerkmale

1. **Responsive Design**: Optimiert für alle Geräte vom Smartphone bis zum Desktop
2. **Animierte UI-Elemente**: Moderne Animationen wie Scroll-Effekte, Flip-Karten und Zählanimationen
3. **Formularvalidierung**: Frontend- und Backend-Validierung für das Kontaktformular
4. **Admin-Bereich**: Benutzerfreundliche Oberfläche zur Verwaltung von Inhalten
5. **Optimierte Performance**: Caching, komprimierte Assets und Lazy-Loading

## Datenmodelle

- **Projekte**: Aktuelle und vergangene Projekte des Clubs
- **News**: Aktuelle Neuigkeiten und Updates
- **Galerie**: Bilder von Veranstaltungen und Aktivitäten
- **Kontakte**: Gespeicherte Kontaktanfragen

## Installation und Setup

1. Repository klonen:
   ```
   git clone <repository-url>
   cd progressive_ladies_club
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

4. Umgebungsvariablen setzen (optional):
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   ```

5. Anwendung starten:
   ```
   flask run
   ```

6. Browser öffnen und zu `http://localhost:5000` navigieren

## Deployment

Für die Produktionsumgebung:

1. Umgebungsvariablen korrekt setzen (SECRET_KEY, MAIL_* Variablen, etc.)
2. Einen WSGI-Server wie Gunicorn verwenden:
   ```
   gunicorn app:app
   ```
3. Mit Nginx oder Apache als Reverse-Proxy konfigurieren

## Entwickelt von

[Ihr Name/Team] - 2023

## Lizenz

Dieses Projekt ist unter der [Lizenz] lizenziert - siehe die LICENSE-Datei für Details. 