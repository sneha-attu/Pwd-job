// Main JavaScript for PWD Job Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializeJobSearch();
    initializeTooltips();
    initializeProgressiveEnhancement();
    
    console.log('PWD Job Portal initialized successfully');
});

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                    field.parentNode.querySelector('.text-danger');
    
    if (!isValid) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    } else {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }
}

// Job search functionality
function initializeJobSearch() {
    const searchInput = document.getElementById('job-search');
    const locationFilter = document.getElementById('location-filter');
    const accessibilityFilter = document.getElementById('accessibility-filter');
    
    if (!searchInput) return;
    
    let searchTimeout;
    
    // Debounced search
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch();
        }, 300);
    });
    
    // Filter changes
    if (locationFilter) {
        locationFilter.addEventListener('change', performSearch);
    }
    
    if (accessibilityFilter) {
        accessibilityFilter.addEventListener('change', performSearch);
    }
}

function performSearch() {
    const searchTerm = document.getElementById('job-search')?.value.toLowerCase() || '';
    const locationFilter = document.getElementById('location-filter')?.value || '';
    const accessibilityFilter = document.getElementById('accessibility-filter')?.value || '';
    
    const jobCards = document.querySelectorAll('.job-card, [data-job-id]');
    let visibleCount = 0;
    
    jobCards.forEach(card => {
        const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
        const company = card.querySelector('.card-subtitle')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
        const location = card.querySelector('[class*="location"]')?.textContent.toLowerCase() || '';
        const hasAccessibility = card.querySelector('.badge.bg-success') !== null;
        
        let show = true;
        
        // Text search
        if (searchTerm && !title.includes(searchTerm) && 
            !company.includes(searchTerm) && !description.includes(searchTerm)) {
            show = false;
        }
        
        // Location filter
        if (locationFilter && !location.includes(locationFilter.toLowerCase())) {
            show = false;
        }
        
        // Accessibility filter
        if (accessibilityFilter === 'accessible' && !hasAccessibility) {
            show = false;
        }
        
        if (show) {
            card.style.display = '';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update results count
    updateResultsCount(visibleCount);
}

function updateResultsCount(count) {
    let resultsInfo = document.getElementById('results-count');
    
    if (!resultsInfo) {
        resultsInfo = document.createElement('p');
        resultsInfo.id = 'results-count';
        resultsInfo.className = 'text-muted small mb-3';
        
        const container = document.querySelector('.row .col-12');
        const jobsContainer = container?.querySelector('.row[id*="job"], .row');
        if (jobsContainer) {
            container.insertBefore(resultsInfo, jobsContainer);
        }
    }
    
    resultsInfo.textContent = `Showing ${count} job${count !== 1 ? 's' : ''}`;
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Progressive enhancement
function initializeProgressiveEnhancement() {
    // Add loading states to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
    
    submitButtons.forEach(button => {
        const form = button.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                button.disabled = true;
            });
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.getElementById('main-content');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
}

function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Export functions for use in other scripts
window.PWDJobPortal = {
    showAlert,
    formatDate,
    performSearch,
    validateField
};
