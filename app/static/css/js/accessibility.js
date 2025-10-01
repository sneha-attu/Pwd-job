// Accessibility Features for PWD Job Portal

class AccessibilityController {
    constructor() {
        this.fontSize = 1;
        this.highContrast = false;
        this.reducedMotion = false;
        
        this.initializeAccessibilityFeatures();
        this.loadUserPreferences();
    }
    
    initializeAccessibilityFeatures() {
        // Font size controls
        document.getElementById('increase-font')?.addEventListener('click', () => this.increaseFontSize());
        document.getElementById('decrease-font')?.addEventListener('click', () => this.decreaseFontSize());
        
        // High contrast toggle
        document.getElementById('high-contrast')?.addEventListener('click', () => this.toggleHighContrast());
        
        // Motion controls
        document.getElementById('pause-animations')?.addEventListener('click', () => this.toggleMotion());
        
        // Keyboard navigation
        this.setupKeyboardNavigation();
        
        // Focus management
        this.setupFocusManagement();
    }
    
    increaseFontSize() {
        if (this.fontSize < 1.5) {
            this.fontSize += 0.25;
            this.applyFontSize();
            this.savePreference('fontSize', this.fontSize);
        }
    }
    
    decreaseFontSize() {
        if (this.fontSize > 0.75) {
            this.fontSize -= 0.25;
            this.applyFontSize();
            this.savePreference('fontSize', this.fontSize);
        }
    }
    
    applyFontSize() {
        document.body.style.fontSize = this.fontSize + 'em';
    }
    
    toggleHighContrast() {
        this.highContrast = !this.highContrast;
        
        if (this.highContrast) {
            document.body.classList.add('high-contrast');
        } else {
            document.body.classList.remove('high-contrast');
        }
        
        this.savePreference('highContrast', this.highContrast);
    }
    
    toggleMotion() {
        this.reducedMotion = !this.reducedMotion;
        
        if (this.reducedMotion) {
            document.body.classList.add('reduce-motion');
        } else {
            document.body.classList.remove('reduce-motion');
        }
        
        this.savePreference('reducedMotion', this.reducedMotion);
    }
    
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Alt + S for search
            if (e.altKey && e.key === 's') {
                e.preventDefault();
                const searchInput = document.getElementById('job-search');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // Alt + N for navigation
            if (e.altKey && e.key === 'n') {
                e.preventDefault();
                const navbar = document.querySelector('.navbar-nav');
                if (navbar) {
                    const firstLink = navbar.querySelector('a');
                    if (firstLink) firstLink.focus();
                }
            }
        });
    }
    
    setupFocusManagement() {
        // Trap focus in modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                const firstInput = modal.querySelector('input, button, textarea, select');
                if (firstInput) firstInput.focus();
            });
        });
    }
    
    savePreference(key, value) {
        localStorage.setItem('pwd_accessibility_' + key, JSON.stringify(value));
    }
    
    loadUserPreferences() {
        // Load font size
        const savedFontSize = localStorage.getItem('pwd_accessibility_fontSize');
        if (savedFontSize) {
            this.fontSize = JSON.parse(savedFontSize);
            this.applyFontSize();
        }
        
        // Load high contrast
        const savedHighContrast = localStorage.getItem('pwd_accessibility_highContrast');
        if (savedHighContrast && JSON.parse(savedHighContrast)) {
            this.toggleHighContrast();
        }
        
        // Load motion preference
        const savedMotion = localStorage.getItem('pwd_accessibility_reducedMotion');
        if (savedMotion && JSON.parse(savedMotion)) {
            this.toggleMotion();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AccessibilityController();
});
