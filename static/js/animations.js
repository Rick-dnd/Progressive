/**
 * Progressive Ladies Club Munich - Animations JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // ScrollReveal-Initialisierung (wenn ScrollReveal in der Seite inkludiert ist)
    if (typeof ScrollReveal !== 'undefined') {
        const sr = ScrollReveal({
            origin: 'bottom',
            distance: '20px',
            duration: 800,
            delay: 200,
            easing: 'ease-in-out',
            reset: false
        });

        // Animationen für verschiedene Elemente
        sr.reveal('.reveal-bottom', { origin: 'bottom' });
        sr.reveal('.reveal-left', { origin: 'left' });
        sr.reveal('.reveal-right', { origin: 'right' });
        sr.reveal('.project-card', { interval: 200 });
        sr.reveal('.gallery-item', { interval: 100 });
    }

    // Partikel-Animation für den Hero-Bereich (Sternenhimmel)
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": 150,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#ffffff"
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": 0.7,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 0.5,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 2,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": false
                },
                "move": {
                    "enable": true,
                    "speed": 0.3,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": true,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "bubble"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "bubble": {
                        "distance": 150,
                        "size": 4,
                        "duration": 2,
                        "opacity": 1,
                        "speed": 3
                    },
                    "push": {
                        "particles_nb": 4
                    }
                }
            },
            "retina_detect": true
        });
    }

    // GSAP Animationen
    if (typeof gsap !== 'undefined') {
        // Animiere die schwebenden Formen
        gsap.to('.shape-1', {
            y: -30,
            x: 10,
            rotation: 5,
            duration: 8,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        });
        
        gsap.to('.shape-2', {
            y: 20,
            x: -15,
            rotation: -8,
            duration: 7,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
            delay: 0.4
        });
        
        gsap.to('.shape-3', {
            y: -15,
            x: -10,
            rotation: 10,
            duration: 9,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
            delay: 0.8
        });
        
        gsap.to('.shape-4', {
            y: 25,
            x: 15,
            rotation: -5,
            duration: 10,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
            delay: 1.2
        });
        
        gsap.to('.shape-5', {
            y: -20,
            x: 20,
            rotation: 8,
            duration: 11,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
            delay: 1.6
        });

        // Animiere die leuchtenden Linien
        gsap.to('.line1', {
            opacity: 0.8,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut"
        });
        
        gsap.to('.line2', {
            opacity: 0.6,
            duration: 3,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut",
            delay: 0.5
        });
        
        gsap.to('.line3', {
            opacity: 0.4,
            duration: 4,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut",
            delay: 1
        });

        // Parallax-Scrolling-Effekt
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            
            // Parallax für Hero-Elemente
            document.querySelectorAll('.floating-shapes .shape').forEach(function(shape, index) {
                const speed = 0.1 + (index * 0.05);
                const yPos = scrollPosition * speed;
                shape.style.transform = `translateY(${yPos}px)`;
            });
            
            document.querySelectorAll('.glow-lines .line').forEach(function(line, index) {
                const speed = 0.2 + (index * 0.05);
                const yPos = scrollPosition * speed;
                line.style.transform = `translateY(${yPos}px) rotate(${line.dataset.rotation || 0}deg)`;
            });
        });
    }

    // Header-Animation beim Scrollen
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // Sternschnuppen-Effekt für den Sternenhimmel
    const heroSection = document.getElementById('hero');
    if (heroSection) {
        // Erstelle die Sternschnuppen-Container
        const shootingStarsContainer = document.createElement('div');
        shootingStarsContainer.className = 'absolute inset-0 overflow-hidden';
        heroSection.appendChild(shootingStarsContainer);
        
        // Funktion zum Erstellen einer Sternschnuppe
        function createShootingStar() {
            const star = document.createElement('div');
            star.className = 'star-shooting';
            
            // Zufällige Position und Verzögerung
            const startX = Math.random() * window.innerWidth;
            const startY = Math.random() * (window.innerHeight / 3); // Nur im oberen Drittel
            star.style.left = startX + 'px';
            star.style.top = startY + 'px';
            star.style.setProperty('--delay', Math.random() * 15); // Zufällige Verzögerung bis zu 15 Sekunden
            
            shootingStarsContainer.appendChild(star);
            
            // Entferne die Sternschnuppe nach der Animation
            setTimeout(() => {
                star.remove();
                createShootingStar(); // Erstelle eine neue Sternschnuppe
            }, 3000 + (Math.random() * 15000)); // 3-18 Sekunden
        }
        
        // Erstelle mehrere Sternschnuppen mit zufälligen Verzögerungen
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                createShootingStar();
            }, Math.random() * 5000);
        }
    }

    // Smooth Scroll für Anker-Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset für den Header
                    behavior: 'smooth'
                });
            }
        });
    });
}); 