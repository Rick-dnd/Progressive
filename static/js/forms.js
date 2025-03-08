/**
 * Progressive Ladies Club Munich - Forms JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Kontaktformular mit AJAX
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Wenn Alpine.js das Formular verarbeitet, nicht weiter verarbeiten
            if (window.Alpine) return;
            
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            // Lade-Status anzeigen
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Wird gesendet...';
            
            // Alle Fehlermeldungen zurücksetzen
            const errorElements = this.querySelectorAll('.error-message');
            errorElements.forEach(el => el.textContent = '');
            
            // AJAX-Anfrage senden
            fetch('/api/contact', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Button-Status zurücksetzen
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                if (data.success) {
                    // Erfolg: Nachricht anzeigen und Formular zurücksetzen
                    showMessage('success', data.message || 'Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden.');
                    contactForm.reset();
                } else {
                    // Fehler: Fehlermeldungen anzeigen
                    if (data.errors) {
                        for (const field in data.errors) {
                            const errorElement = document.getElementById(`${field}-error`);
                            if (errorElement) {
                                errorElement.textContent = data.errors[field];
                            }
                        }
                    } else {
                        showMessage('error', 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.');
                    }
                }
            })
            .catch(error => {
                // Bei Netzwerkfehlern
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                showMessage('error', 'Ein Netzwerkfehler ist aufgetreten. Bitte versuchen Sie es später erneut.');
                console.error('Error:', error);
            });
        });
    }
    
    // Hilfsfunktion zum Anzeigen von Erfolgs- oder Fehlermeldungen
    function showMessage(type, text) {
        // Entferne vorherige Nachrichten
        const existingMessages = document.querySelectorAll('.form-message');
        existingMessages.forEach(msg => msg.remove());
        
        // Neue Nachricht erstellen
        const messageElement = document.createElement('div');
        messageElement.className = `form-message ${type === 'success' ? 'form-message-success' : 'form-message-error'}`;
        messageElement.textContent = text;
        
        // Nachricht nach dem Formular einfügen
        contactForm.after(messageElement);
        
        // Nachricht nach einiger Zeit ausblenden
        setTimeout(() => {
            messageElement.classList.add('fade-out');
            setTimeout(() => messageElement.remove(), 500);
        }, 5000);
    }
    
    // Formularvalidierung für Echtzeit-Feedback
    const inputs = document.querySelectorAll('.validate-input');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            // Wenn bereits validiert, bei Eingabe neu validieren
            if (this.dataset.validated === 'true') {
                validateField(this);
            }
        });
    });
    
    function validateField(field) {
        field.dataset.validated = 'true';
        const errorElement = document.getElementById(`${field.name}-error`);
        if (!errorElement) return;
        
        // Einfache Validierungsregeln
        if (field.required && !field.value.trim()) {
            errorElement.textContent = 'Dieses Feld ist erforderlich.';
            return false;
        }
        
        if (field.type === 'email' && field.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                errorElement.textContent = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.';
                return false;
            }
        }
        
        // Wenn keine Fehler, Fehlermeldung zurücksetzen
        errorElement.textContent = '';
        return true;
    }
}); 