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
    
    // Projekte Navigation
    const prevProjectBtn = document.getElementById('prev-project');
    const nextProjectBtn = document.getElementById('next-project');
    const projectsContainer = document.getElementById('projects-container');
    
    const prevPastProjectBtn = document.getElementById('prev-past-project');
    const nextPastProjectBtn = document.getElementById('next-past-project');
    const pastProjectsContainer = document.getElementById('past-projects-container');
    
    console.log('DOM Elemente gefunden:', {
        prevProjectBtn: !!prevProjectBtn,
        nextProjectBtn: !!nextProjectBtn,
        projectsContainer: !!projectsContainer,
        prevPastProjectBtn: !!prevPastProjectBtn,
        nextPastProjectBtn: !!nextPastProjectBtn,
        pastProjectsContainer: !!pastProjectsContainer
    });
    
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
});

// Funktion für die Projekt-Navigation
function setupProjectNavigation(prevBtn, nextBtn, container) {
    if (!prevBtn || !nextBtn || !container) return;
    
    const projectCards = container.querySelectorAll('.project-card');
    if (projectCards.length === 0) return;
    
    let currentPage = 0;
    let projectsPerView = 1;
    
    // Bestimme die Anzahl anzuzeigender Projekte basierend auf der Bildschirmbreite
    function updateProjectsPerView() {
        if (window.innerWidth >= 1024) { // lg
            projectsPerView = 3;
        } else if (window.innerWidth >= 768) { // md
            projectsPerView = 2;
        } else {
            projectsPerView = 1; // sm
        }
    }
    
    // Initial festlegen
    updateProjectsPerView();
    
    // Bei Größenänderung des Fensters aktualisieren
    window.addEventListener('resize', () => {
        updateProjectsPerView();
        moveToPage(currentPage); // Aktuelle Seite neu berechnen und anzeigen
    });
    
    const totalPages = Math.ceil(projectCards.length / projectsPerView) - 1;
    
    // Navigation-Buttons aktualisieren
    const updateNavButtons = () => {
        // Verstecke oder zeige Pfeil-Buttons basierend auf der aktuellen Seite
        if (currentPage === 0) {
            // Erste Seite - nur Vorwärts-Button anzeigen
            prevBtn.style.opacity = '0';
            prevBtn.style.pointerEvents = 'none';
            nextBtn.style.opacity = '1';
            nextBtn.style.pointerEvents = 'auto';
        } else if (currentPage >= totalPages) {
            // Letzte Seite - nur Rückwärts-Button anzeigen
            prevBtn.style.opacity = '1';
            prevBtn.style.pointerEvents = 'auto';
            nextBtn.style.opacity = '0';
            nextBtn.style.pointerEvents = 'none';
        } else {
            // Mittlere Seite - beide Buttons anzeigen
            prevBtn.style.opacity = '1';
            prevBtn.style.pointerEvents = 'auto';
            nextBtn.style.opacity = '1';
            nextBtn.style.pointerEvents = 'auto';
        }
    };
    
    // Indikator-Punkte generieren und aktualisieren
    const updateIndicators = () => {
        // Finde den richtigen Indikator-Container (unterschiedliche IDs für aktuelle/vergangene Projekte)
        let indicatorContainerId;
        if (container.id === 'projects-container') {
            indicatorContainerId = 'project-indicators';
        } else if (container.id === 'past-projects-container') {
            indicatorContainerId = 'past-project-indicators';
        } else {
            console.warn('Unbekannter Container: ' + container.id);
            return;
        }
        
        // Finde das Indikator-Container-Element
        const indicatorContainer = container.closest('.relative').querySelector('#' + indicatorContainerId);
        if (!indicatorContainer) {
            console.warn('Indikator-Container nicht gefunden: #' + indicatorContainerId);
            return;
        }
        
        // Leere den Container
        indicatorContainer.innerHTML = '';
        
        // Berechne die Anzahl der Seiten
        const pageCount = Math.max(1, Math.ceil(projectCards.length / projectsPerView));
        
        // Füge für jede Seite einen Indikator hinzu
        for (let i = 0; i < pageCount; i++) {
            const indicator = document.createElement('span');
            indicator.classList.add('w-3', 'h-3', 'rounded-full', 'transition-all', 'duration-300');
            
            // Aktive Seite hervorheben
            if (i === currentPage) {
                indicator.classList.add('bg-primary', 'transform', 'scale-110');
            } else {
                indicator.classList.add('bg-gray-300');
            }
            
            // Event-Listener für Klick auf den Indikator
            indicator.addEventListener('click', () => {
                moveToPage(i);
            });
            
            // Hover-Effekt
            indicator.style.cursor = 'pointer';
            
            // Zum Container hinzufügen
            indicatorContainer.appendChild(indicator);
        }
        
        console.log(`Indikatoren aktualisiert für ${indicatorContainerId}: ${pageCount} Seiten, aktuelle Seite: ${currentPage}`);
    };
    
    // Projekte aktualisieren - vereinfachte Berechnung
    const moveToPage = (page) => {
        if (page < 0) page = 0;
        if (page > totalPages) page = totalPages;
        
        // Aktuelle Seitennummer aktualisieren
        currentPage = page;
        
        // Einfache fixe Berechnung für den Karussell-Offset
        const cardWidth = projectCards[0].offsetWidth;
        const gapWidth = 32; // Entspricht gap-8 (8 * 4px)
        
        // Berechne wieviele Karten wir verschieben müssen
        const cardsToMove = currentPage * projectsPerView;
        
        // Berechne den Offset basierend auf der Kartenanzahl
        // Verhindere Überscrolling, wenn nicht genug Karten übrig sind
        const maxCardsToMove = Math.min(cardsToMove, projectCards.length - projectsPerView);
        const offset = Math.max(0, maxCardsToMove * (cardWidth + gapWidth));
        
        // Container horizontal verschieben
        container.style.transform = `translateX(-${offset}px)`;
        
        // Buttons und Indikatoren aktualisieren
        updateNavButtons();
        updateIndicators();
        console.log(`Navigation zur Seite ${currentPage}/${totalPages}, Offset: ${offset}px, Karten: ${projectCards.length}`);
    };
    
    // Initial setup
    moveToPage(0);
    
    // Event Listener für Buttons mit Event Capture
    prevBtn.addEventListener('click', function(event) {
        console.log("Zurück-Button geklickt");
        event.preventDefault();
        if (currentPage > 0) {
            moveToPage(currentPage - 1);
        }
    }, true);
    
    nextBtn.addEventListener('click', function(event) {
        console.log("Weiter-Button geklickt");
        event.preventDefault();
        if (currentPage < totalPages) {
            moveToPage(currentPage + 1);
        }
    }, true);
    
    // Initial die Navigationspfeile aktualisieren
    updateNavButtons();
} 