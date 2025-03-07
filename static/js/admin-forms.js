// Admin-Formular-Funktionalitäten

// Mapping von deutschen Schlüsselwörtern zu Font Awesome Icons
const keywordToIconMap = {
    // Kinder bezogene Begriffe
    'kind': 'fa-child',
    'kinder': 'fa-child',
    'kindern': 'fa-child',
    'kinderhilfe': 'fa-hands-helping',
    'jugend': 'fa-child',
    'jugendliche': 'fa-child',
    
    // Allgemeine Begriffe
    'projekt': 'fa-project-diagram',
    'bildung': 'fa-graduation-cap',
    'schule': 'fa-school',
    'universität': 'fa-university',
    'lehre': 'fa-chalkboard-teacher',
    'forschung': 'fa-microscope',
    'gesundheit': 'fa-heartbeat',
    'medizin': 'fa-stethoscope',
    'krankenhaus': 'fa-hospital',
    'umwelt': 'fa-leaf',
    'natur': 'fa-tree',
    'klima': 'fa-cloud-sun',
    'recycling': 'fa-recycle',
    'energie': 'fa-bolt',
    'solar': 'fa-solar-panel',
    'wasser': 'fa-water',
    'wind': 'fa-wind',
    'kultur': 'fa-theater-masks',
    'kunst': 'fa-palette',
    'musik': 'fa-music',
    'tanz': 'fa-dancing',
    'literatur': 'fa-book',
    'sport': 'fa-running',
    'fußball': 'fa-futbol',
    'basketball': 'fa-basketball-ball',
    'tennis': 'fa-tennis',
    'schwimmen': 'fa-swimming-pool',
    'technologie': 'fa-microchip',
    'computer': 'fa-laptop',
    'software': 'fa-code',
    'internet': 'fa-globe',
    'netzwerk': 'fa-network-wired',
    'kommunikation': 'fa-comments',
    'telefon': 'fa-phone',
    'handy': 'fa-mobile-alt',
    'sozial': 'fa-hands-helping',
    'gemeinschaft': 'fa-users',
    'hilfe': 'fa-hand-holding-heart',
    'unterstützung': 'fa-hands-helping',
    'spende': 'fa-donate',
    'freiwillig': 'fa-hand-holding-heart',
    'wissenschaft': 'fa-atom',
    'physik': 'fa-atom',
    'chemie': 'fa-flask',
    'biologie': 'fa-dna',
    'mathematik': 'fa-calculator',
    'wirtschaft': 'fa-chart-line',
    'finanzen': 'fa-coins',
    'bank': 'fa-landmark',
    'geld': 'fa-money-bill-wave',
    'investition': 'fa-chart-line',
    'recht': 'fa-balance-scale',
    'gesetz': 'fa-gavel',
    'politik': 'fa-vote-yea',
    'regierung': 'fa-landmark',
    'demokratie': 'fa-flag',
    'reise': 'fa-plane',
    'urlaub': 'fa-umbrella-beach',
    'hotel': 'fa-hotel',
    'flug': 'fa-plane',
    'zug': 'fa-train',
    'auto': 'fa-car',
    'essen': 'fa-utensils',
    'restaurant': 'fa-utensils',
    'lebensmittel': 'fa-apple-alt',
    'kochen': 'fa-cookie',
    'bäckerei': 'fa-bread-slice',
    'kaffee': 'fa-coffee',
    'wohnen': 'fa-home',
    'haus': 'fa-house',
    'wohnung': 'fa-building',
    'möbel': 'fa-couch',
    'garten': 'fa-seedling',
    'mode': 'fa-tshirt',
    'kleidung': 'fa-tshirt',
    'schuhe': 'fa-shoe-prints',
    'schmuck': 'fa-gem',
    'schönheit': 'fa-spa',
    'kosmetik': 'fa-kiss',
    'haar': 'fa-cut',
    'familie': 'fa-users',
    'baby': 'fa-baby',
    'hochzeit': 'fa-ring',
    'liebe': 'fa-heart',
    'freundschaft': 'fa-user-friends',
    'tiere': 'fa-paw',
    'hund': 'fa-dog',
    'katze': 'fa-cat',
    'haustier': 'fa-paw',
    'religion': 'fa-pray',
    'kirche': 'fa-church',
    'moschee': 'fa-mosque',
    'synagoge': 'fa-synagogue',
    'glaube': 'fa-hands',
    'handwerk': 'fa-tools',
    'qualität': 'fa-check-circle'
};

// Standardicon, wenn kein passendes gefunden wird
const defaultIcon = 'fa-project-diagram';

/**
 * Findet ein passendes Icon basierend auf dem Projekttitel
 * @param {string} title - Der Titel des Projekts
 * @returns {string} - Font Awesome Icon-Klasse
 */
function findMatchingIcon(title) {
    if (!title) {
        console.log("Kein Titel angegeben, verwende Standard-Icon:", defaultIcon);
        return defaultIcon;
    }
    
    title = title.toLowerCase();
    console.log("Suche nach Icon für Titel:", title);
    
    // Spezifische Phrasen-Erkennung
    const specialPhrases = {
        'hilfe für kinder': 'fa-child',
        'kinderhilfe': 'fa-child',
        'hilfe für kind': 'fa-child',
        'unterstützung für kinder': 'fa-child',
        'kinder unterstützen': 'fa-child',
        'für kinder': 'fa-child',
        'kinder': 'fa-child',
        'kind': 'fa-child'
    };
    
    // Prüfe auf exakte Phrasen
    for (const [phrase, icon] of Object.entries(specialPhrases)) {
        if (title.includes(phrase)) {
            console.log("Spezielle Phrase erkannt:", phrase, "->", icon);
            return icon;
        }
    }
    
    // Suche nach Übereinstimmungen mit Schlüsselwörtern
    for (const [keyword, icon] of Object.entries(keywordToIconMap)) {
        if (title.includes(keyword.toLowerCase())) {
            console.log("Icon gefunden für Schlüsselwort:", keyword, "->", icon);
            return icon;
        }
    }
    
    console.log("Kein passendes Icon gefunden, verwende Standard:", defaultIcon);
    return defaultIcon;
}

/**
 * Aktualisiert die Icon-Vorschau
 * @param {string} [iconClass] - Optional: Die Icon-Klasse, die angezeigt werden soll
 */
function updateIconPreview(iconClass) {
    const iconInput = document.getElementById('icon');
    const iconPreview = document.getElementById('icon-preview');
    
    if (iconInput && iconPreview) {
        // Wenn eine spezifische Icon-Klasse übergeben wurde, verwende diese
        // ansonsten nimm den Wert aus dem Icon-Eingabefeld
        const iconToShow = iconClass || iconInput.value || defaultIcon;
        
        // Leere das Icon-Element und füge die entsprechenden Klassen hinzu
        iconPreview.innerHTML = '';
        const iconElement = document.createElement('i');
        iconElement.className = 'fas ' + iconToShow;
        iconPreview.appendChild(iconElement);
        
        // Wenn keine Icon-Klasse übergeben wurde, aktualisiere das Eingabefeld
        if (!iconClass && (!iconInput.value || iconInput.value.trim() === '')) {
            iconInput.value = defaultIcon;
        }
        
        console.log("Icon-Vorschau aktualisiert:", iconToShow);
    } else {
        console.warn("Icon-Eingabe oder Vorschau-Element nicht gefunden");
    }
}

/**
 * Zeigt den Icon-Auswahl-Dialog an
 */
function showIconPicker() {
    const modal = document.getElementById('icon-picker-modal');
    if (modal) {
        modal.style.display = 'block';
    }
}

/**
 * Schließt den Icon-Auswahl-Dialog
 */
function closeIconPicker() {
    const modal = document.getElementById('icon-picker-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

/**
 * Wählt ein Icon aus und schließt den Dialog
 * @param {string} iconClass - Die Klasse des ausgewählten Icons
 */
function selectIcon(iconClass) {
    const iconInput = document.getElementById('icon');
    if (iconInput) {
        iconInput.value = iconClass;
        updateIconPreview(iconClass);
    }
    closeIconPicker();
}

/**
 * Initialisiert die automatische Icon-Auswahl
 */
function initAutoIconSelect() {
    console.log("Initialisiere automatische Icon-Auswahl");
    const titleInput = document.getElementById('title');
    const iconInput = document.getElementById('icon');
    const iconBtn = document.getElementById('icon-picker-btn');
    const iconPreview = document.getElementById('icon-preview');
    
    if (titleInput && iconInput) {
        console.log("Titel- und Icon-Eingabefelder gefunden");
        
        // IMMER sicherstellen, dass das Icon-Feld einen Wert hat
        if (!iconInput.value || iconInput.value.trim() === '') {
            // Prüfe zuerst, ob wir einen Titel haben
            if (titleInput.value && titleInput.value.trim() !== '') {
                const matchingIcon = findMatchingIcon(titleInput.value);
                iconInput.value = matchingIcon;
                console.log("Setze Icon basierend auf existierendem Titel:", matchingIcon);
            } else {
                // Wenn kein Titel, setze Standard-Icon
                iconInput.value = defaultIcon;
                console.log("Kein Titel vorhanden, setze Standard-Icon:", defaultIcon);
            }
            // Aktualisiere in jedem Fall die Vorschau
            updateIconPreview(iconInput.value);
        }
        
        // Listener für Titeländerungen hinzufügen
        titleInput.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                const matchingIcon = findMatchingIcon(this.value);
                console.log("Passendes Icon gefunden:", matchingIcon, "für Titel:", this.value);
                iconInput.value = matchingIcon;
                updateIconPreview(matchingIcon);
            } else {
                // Wenn der Titel leer ist, verwende das Standardicon
                iconInput.value = defaultIcon;
                updateIconPreview(defaultIcon);
            }
        });
        
        // Sofort die Vorschau aktualisieren
        updateIconPreview(iconInput.value || defaultIcon);
        
        // Icon-Wähler-Button
        if (iconBtn) {
            iconBtn.addEventListener('click', function(e) {
                e.preventDefault();
                showIconPicker();
            });
        }
    } else {
        console.warn("Titel- oder Icon-Eingabefeld nicht gefunden");
    }
}

// Initialisierung bei Dokumentenladung
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM vollständig geladen");
    
    // Initialisiere die Editoren
    initSummernote();
    
    // Initialisiere den Icon-Selector
    initIconSelector();
    
    // Initialisiere die automatische Icon-Auswahl
    initAutoIconSelect();
    
    // Initialisiere die Farblauswahl
    initColorPicker();

    // Verzögerte erneute Initialisierung (manchmal werden Komponenten später geladen)
    setTimeout(function() {
        console.log("Verzögerte Initialisierung der Icon-Auswahl");
        // Aktualisiere die Icon-Vorschau ein weiteres Mal
        const iconInput = document.getElementById('icon');
        if (iconInput) {
            console.log("Aktualisiere Icon nochmal:", iconInput.value);
            updateIconPreview(iconInput.value || defaultIcon);
        }
        
        // Initialisiere nochmal die automatische Icon-Auswahl
        initAutoIconSelect();
        
        // Löse einen künstlichen Input-Event aus, wenn das Titelfeld einen Wert hat
        const titleInput = document.getElementById('title');
        if (titleInput && titleInput.value.trim() !== '') {
            console.log("Löse künstlichen Input-Event auf Titelfeld aus:", titleInput.value);
            const event = new Event('input');
            titleInput.dispatchEvent(event);
        }
    }, 500);
}); 