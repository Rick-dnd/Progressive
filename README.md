# Elegant Progressive Ladies Club Munich e.V. - Website

Eine moderne, responsive One-Page-Website für den Elegant Progressive Ladies Club Munich e.V., entwickelt mit Flask, TailwindCSS und Alpine.js.

---

# Elegant Progressive Ladies Club Munich e.V. - Website

A modern, responsive one-page website for the Elegant Progressive Ladies Club Munich e.V., developed with Flask, TailwindCSS, and Alpine.js.

## Projektübersicht / Project Overview

**DE:**  
Diese Website wurde entwickelt, um die Mission, Projekte und Aktivitäten des Progressive Ladies Club zu präsentieren. Die Seite ist als One-Page-Webanwendung konzipiert, die verschiedene Abschnitte wie Über Uns, Projekte, News und Kontakt in einer einzigen, elegant scrollbaren Seite vereint.

**EN:**  
This website was developed to present the mission, projects, and activities of the Progressive Ladies Club. The page is designed as a one-page web application that combines various sections such as About Us, Projects, News, and Contact in a single, elegantly scrollable page.

## Technologiestack / Technology Stack

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

## Projektstruktur / Project Structure

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

## Implementierte Sicherheitsmaßnahmen / Implemented Security Measures

**DE:**  
Die Website ist mit mehreren Sicherheitsmaßnahmen ausgestattet, um die Daten und Benutzer zu schützen:

1. **Content Security Policy (CSP)**: Durch Implementierung von Flask-Talisman wird eine strenge Content Security Policy erzwungen, die XSS-Angriffe verhindert.
2. **CSRF-Protection**: Alle Formulare sind mit CSRF-Token geschützt, um Cross-Site Request Forgery Angriffe zu verhindern.
3. **HTML-Sanitization**: Benutzereingaben werden mit Bleach sanitisiert, um XSS-Angriffe zu vermeiden.
4. **Sichere HTTP-Header**: HTTP-Strict-Transport-Security (HSTS) und andere Sicherheitsheader sind aktiviert.
5. **Sichere Cookie-Einstellungen**: HttpOnly und Secure Flags für Cookies sind aktiviert.
6. **Input-Validierung**: Strenge Validierung von Eingabedaten auf Server- und Client-Seite.
7. **Parametrisierte SQL-Abfragen**: Verwendung von SQLAlchemy ORM verhindert SQL-Injection.

**EN:**  
The website is equipped with several security measures to protect data and users:

1. **Content Security Policy (CSP)**: Implementation of Flask-Talisman enforces a strict content security policy that prevents XSS attacks.
2. **CSRF Protection**: All forms are protected with CSRF tokens to prevent cross-site request forgery attacks.
3. **HTML Sanitization**: User inputs are sanitized with Bleach to prevent XSS attacks.
4. **Secure HTTP Headers**: HTTP Strict Transport Security (HSTS) and other security headers are enabled.
5. **Secure Cookie Settings**: HttpOnly and Secure flags for cookies are enabled.
6. **Input Validation**: Strict validation of input data on both server and client side.
7. **Parameterized SQL Queries**: Use of SQLAlchemy ORM prevents SQL injection.

## SEO & Performance Optimierungen / SEO & Performance Optimizations

**DE:**  
Die Website wurde für Suchmaschinen optimiert und für maximale Performance ausgelegt:

### SEO-Optimierungen:
1. **Mehrsprachige Meta-Tags**: Optimierte Meta-Tags für Deutsch und Englisch.
2. **Strukturierte Daten mit JSON-LD**: Implementation von strukturierten Daten für verbesserte Rich Snippets in Suchergebnissen.
3. **Hreflang-Attribute**: Korrekte Sprachzuweisung für internationale Zielgruppen.
4. **Kanonische URLs**: Vermeidung von Duplicate Content.
5. **Optimierte URL-Struktur**: Klare, suchmaschinenfreundliche URLs.
6. **Semantisches HTML**: Verwendung von HTML5-Elementen für bessere Inhaltsbewertung.
7. **Sitemap.xml & robots.txt**: Optimierter Zugang für Suchmaschinenroboter.
8. **Meta-Tags für Social Media**: Open Graph und Twitter Cards für bessere Darstellung in sozialen Medien.

### Backlink-Strategie:
1. **Partnerverlinkungen**: Strategische Links zu relevanten Partnerorganisationen.
2. **Lokale SEO**: Verlinkungen zu städtischen Ressourcen und lokalen Organisationen.
3. **Soziale Netzwerke**: Integrierte Social-Media-Links zur Steigerung der Reichweite.
4. **Branchen-Ressourcen**: Verlinkungen zu themenverwandten Websites.

### Performance-Optimierungen:
1. **Lazy-Loading für Bilder**: Beschleunigtes Laden der Startseite.
2. **Minifizierung von CSS/JS**: Reduzierung der Dateigrößen für schnellere Ladezeiten.
3. **Responsive Bilder**: Optimierte Bildgrößen für verschiedene Endgeräte.
4. **Browser-Caching**: Verbesserte Cache-Control Header für wiederkehrende Besucher.
5. **Optimierte Schriftarten**: Einbettung nur notwendiger Schriftarten und Varianten.
6. **Reduzierung externer Requests**: Konsolidierung von externen Ressourcen.

**EN:**  
The website has been optimized for search engines and designed for maximum performance:

### SEO Optimizations:
1. **Multilingual Meta Tags**: Optimized meta tags for German and English.
2. **Structured Data with JSON-LD**: Implementation of structured data for improved rich snippets in search results.
3. **Hreflang Attributes**: Correct language assignment for international audiences.
4. **Canonical URLs**: Avoidance of duplicate content.
5. **Optimized URL Structure**: Clear, search engine friendly URLs.
6. **Semantic HTML**: Use of HTML5 elements for better content evaluation.
7. **Sitemap.xml & robots.txt**: Optimized access for search engine robots.
8. **Meta Tags for Social Media**: Open Graph and Twitter Cards for better representation in social media.

### Backlink Strategy:
1. **Partner Links**: Strategic links to relevant partner organizations.
2. **Local SEO**: Links to municipal resources and local organizations.
3. **Social Networks**: Integrated social media links to increase reach.
4. **Industry Resources**: Links to thematically related websites.

### Performance Optimizations:
1. **Lazy Loading for Images**: Accelerated loading of the home page.
2. **Minification of CSS/JS**: Reduction of file sizes for faster loading times.
3. **Responsive Images**: Optimized image sizes for different devices.
4. **Browser Caching**: Improved cache-control headers for returning visitors.
5. **Optimized Fonts**: Embedding only necessary fonts and variants.
6. **Reduction of External Requests**: Consolidation of external resources.

## Mehrsprachigkeit / Multilingualism

**DE:**  
Die Website unterstützt mehrere Sprachen, um ein breiteres Publikum zu erreichen:

1. **Sprachumschalter**: Einfacher Wechsel zwischen Deutsch und Englisch.
2. **Dynamische Inhalte**: Alle Texte werden basierend auf der gewählten Sprache angepasst.
3. **Hreflang-Attribute**: Korrekte Sprachzuweisung für Suchmaschinen.
4. **Zweisprachige Meta-Tags**: Optimierte Meta-Informationen in beiden Sprachen.
5. **Lokalisierte URLs**: Klare URL-Struktur mit Sprachpräfixen für bessere Benutzererfahrung.

**EN:**  
The website supports multiple languages to reach a wider audience:

1. **Language Switcher**: Easy switching between German and English.
2. **Dynamic Content**: All texts are adapted based on the selected language.
3. **Hreflang Attributes**: Correct language assignment for search engines.
4. **Bilingual Meta Tags**: Optimized meta information in both languages.
5. **Localized URLs**: Clear URL structure with language prefixes for better user experience.

## Hauptmerkmale / Main Features

1. **Responsive Design**: Optimiert für alle Geräte vom Smartphone bis zum Desktop
2. **Animierte UI-Elemente**: Moderne Animationen wie Scroll-Effekte, Flip-Karten und Zählanimationen
3. **Formularvalidierung**: Frontend- und Backend-Validierung für das Kontaktformular
4. **Admin-Bereich**: Benutzerfreundliche Oberfläche zur Verwaltung von Inhalten
5. **Optimierte Performance**: Caching, komprimierte Assets und Lazy-Loading
6. **Mehrsprachige Unterstützung**: Vollständige Unterstützung für Deutsch und Englisch
7. **SEO-Optimierung**: Strukturierte Daten, Meta-Tags und optimierte URL-Struktur

## Datenmodelle / Data Models

- **Projekte**: Aktuelle und vergangene Projekte des Clubs
- **News**: Aktuelle Neuigkeiten und Updates
- **Galerie**: Bilder von Veranstaltungen und Aktivitäten
- **Kontakte**: Gespeicherte Kontaktanfragen

## Installation und Setup / Installation and Setup

1. Repository klonen / Clone repository:
   ```
   git clone <repository-url>
   cd progressive_ladies_club
   ```

2. Virtuelle Umgebung erstellen und aktivieren / Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren / Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Umgebungsvariablen setzen (optional) / Set environment variables (optional):
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   ```

5. Anwendung starten / Start application:
   ```
   flask run
   ```

6. Browser öffnen und zu `http://localhost:5000` navigieren / Open browser and navigate to `http://localhost:5000`

## Deployment

Für die Produktionsumgebung / For the production environment:

1. Umgebungsvariablen korrekt setzen / Set environment variables correctly (SECRET_KEY, MAIL_* Variablen, etc.)
2. Einen WSGI-Server wie Gunicorn verwenden / Use a WSGI server like Gunicorn:
   ```
   gunicorn app:app
   ```
3. Mit Nginx oder Apache als Reverse-Proxy konfigurieren / Configure with Nginx or Apache as reverse proxy

## Entwickelt von / Developed by

[Ihr Name/Team] - 2023

## Lizenz / License

Dieses Projekt ist unter der [Lizenz] lizenziert - siehe die LICENSE-Datei für Details.
This project is licensed under the [License] - see the LICENSE file for details. 