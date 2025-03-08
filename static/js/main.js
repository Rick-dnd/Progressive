/**
 * Progressive Ladies Club Munich - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Alpine.js verfügbar machen (wenn nicht über CDN eingebunden)
    if (typeof Alpine === 'undefined') {
        console.warn('Alpine.js ist nicht verfügbar. Einige Funktionen könnten beeinträchtigt sein.');
    }
    
    // Aktuellen Menüpunkt basierend auf Scroll-Position hervorheben
    function updateActiveMenuItem() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let currentSectionId = '';
        const scrollPosition = window.scrollY + 100; // Offset für den Header
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${currentSectionId}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Menüelemente aktualisieren beim Scrollen
    window.addEventListener('scroll', updateActiveMenuItem);
    updateActiveMenuItem(); // Initial ausführen
    
    // Burger-Menü-Funktionalität (wenn nicht durch Alpine.js verwaltet)
    const burgerButton = document.querySelector('.burger-menu');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (burgerButton && mobileMenu && !window.Alpine) {
        burgerButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            burgerButton.classList.toggle('active');
        });
        
        // Schließen des mobilen Menüs bei Klick auf Links
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                burgerButton.classList.remove('active');
            });
        });
    }
    
    // Lazy Loading für Bilder
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('.lazy-img');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-img');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Aktuelle Jahreszahl im Footer aktualisieren
    const yearElements = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    
    yearElements.forEach(element => {
        element.textContent = currentYear;
    });
    
    // Verbesserte Hover-Interaktion für das Vereinsbild
    const aboutImageContainer = document.querySelector('.about-image-container');
    if (aboutImageContainer) {
        // Mouseenter-Event für Desktop
        aboutImageContainer.addEventListener('mouseenter', function() {
            this.classList.add('hover-active');
        });
        
        // Mouseleave-Event für Desktop
        aboutImageContainer.addEventListener('mouseleave', function() {
            this.classList.remove('hover-active');
        });
        
        // Touch-Events für mobile Geräte
        aboutImageContainer.addEventListener('touchstart', function(e) {
            e.preventDefault();
            this.classList.add('hover-active');
        });
        
        aboutImageContainer.addEventListener('touchend', function() {
            setTimeout(() => {
                this.classList.remove('hover-active');
            }, 500);
        });
    }
    
    // Projektfilter
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-card');
    
    if (filterButtons.length > 0 && projectItems.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.getAttribute('data-filter');
                
                // Aktive Klasse für Buttons aktualisieren
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Projekte filtern
                projectItems.forEach(item => {
                    if (filter === 'all') {
                        item.style.display = 'block';
                    } else {
                        if (item.classList.contains(filter)) {
                            item.style.display = 'block';
                        } else {
                            item.style.display = 'none';
                        }
                    }
                });
            });
        });
    }
    
    // Kontaktformular-Validierung
    const contactForm = document.getElementById('contact-form');
    if (contactForm && !window.Alpine) {
        contactForm.querySelectorAll('input, textarea').forEach(field => {
            // Labels verschieben, wenn Feldinhalt vorhanden ist
            if (field.value) {
                const label = field.parentNode.querySelector('label');
                if (label) {
                    label.classList.add('active');
                }
            }
            
            // Event Listener für Fokus
            field.addEventListener('focus', function() {
                const label = this.parentNode.querySelector('label');
                if (label) {
                    label.classList.add('active');
                }
            });
            
            // Event Listener für Blur
            field.addEventListener('blur', function() {
                if (!this.value) {
                    const label = this.parentNode.querySelector('label');
                    if (label) {
                        label.classList.remove('active');
                    }
                }
            });
        });
    }
    
    // Projekte Navigation initialisieren
    console.log('Navigation initialisieren...');
    
    // Projekte Navigation - jetzt deaktiviert, da wir ein Grid-Layout verwenden
    const prevProjectBtn = document.getElementById('prev-project');
    const nextProjectBtn = document.getElementById('next-project');
    const projectsContainer = document.getElementById('projects-container');
    
    const prevPastProjectBtn = document.getElementById('prev-past-project');
    const nextPastProjectBtn = document.getElementById('next-past-project');
    const pastProjectsContainer = document.getElementById('past-projects-container');
    
    console.log('DOM Elemente gefunden (diese werden nicht mehr für das Karussell verwendet):', {
        prevProjectBtn: !!prevProjectBtn,
        nextProjectBtn: !!nextProjectBtn,
        projectsContainer: !!projectsContainer,
        prevPastProjectBtn: !!prevPastProjectBtn,
        nextPastProjectBtn: !!nextPastProjectBtn,
        pastProjectsContainer: !!pastProjectsContainer
    });
    
    // Karussell-Navigation ist jetzt deaktiviert, da wir ein Grid-Layout verwenden
    /*
    // Navigationen initialisieren
    if (prevProjectBtn && nextProjectBtn && projectsContainer) {
        console.log('Aktuelle Projekte Navigation wird initialisiert');
        setupProjectNavigation(prevProjectBtn, nextProjectBtn, projectsContainer);
    } else {
        console.warn('Einige Elemente für Aktuelle Projekte Navigation fehlen!');
    }
    
    if (prevPastProjectBtn && nextPastProjectBtn && pastProjectsContainer) {
        console.log('Vergangene Projekte Navigation wird initialisiert');
        setupProjectNavigation(prevPastProjectBtn, nextPastProjectBtn, pastProjectsContainer);
    } else {
        console.warn('Einige Elemente für Vergangene Projekte Navigation fehlen!');
    }
    */
});

// Funktion für die Projekt-Navigation - nicht mehr verwendet, da wir ein Grid-Layout nutzen
/* 
function setupProjectNavigation(prevBtn, nextBtn, container) {
    // Code auskommentiert, da wir jetzt ein Grid-Layout verwenden
}
*/ 