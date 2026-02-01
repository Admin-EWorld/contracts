// ================================
// Contract Generator - Main JavaScript
// ================================

// Theme Management
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
    }
}

// Form Validation
class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.errors = {};
        this.init();
    }

    init() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Real-time validation
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const name = field.name;
        let error = null;

        // Required validation
        if (field.hasAttribute('required') && !value) {
            error = 'This field is required';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                error = 'Please enter a valid email address';
            }
        }

        // Number validation
        if (field.type === 'number' && value) {
            const num = parseFloat(value);
            if (isNaN(num) || num <= 0) {
                error = 'Please enter a valid positive number';
            }
        }

        // Fee amount validation
        if (name === 'fees' && value) {
            const cleanValue = value.replace(/,/g, '');
            const num = parseFloat(cleanValue);
            if (isNaN(num) || num <= 0) {
                error = 'Please enter a valid fee amount';
            }
        }

        // Service selection validation
        if (name === 'services') {
            const checkedServices = this.form.querySelectorAll('input[name="services"]:checked');
            if (checkedServices.length === 0) {
                error = 'Please select at least one service';
            }
        }

        if (error) {
            this.showError(field, error);
            return false;
        } else {
            this.clearError(field);
            return true;
        }
    }

    showError(field, message) {
        this.errors[field.name] = message;
        field.classList.add('error');

        let errorElement = field.parentElement.querySelector('.form-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'form-error';
            field.parentElement.appendChild(errorElement);
        }
        errorElement.textContent = message;
        errorElement.classList.add('visible');
    }

    clearError(field) {
        delete this.errors[field.name];
        field.classList.remove('error');

        const errorElement = field.parentElement.querySelector('.form-error');
        if (errorElement) {
            errorElement.classList.remove('visible');
        }
    }

    validateForm() {
        this.errors = {};
        const inputs = this.form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        // Validate at least one service is selected
        const checkedServices = this.form.querySelectorAll('input[name="services"]:checked');
        if (checkedServices.length === 0) {
            isValid = false;
            const servicesContainer = this.form.querySelector('.checkbox-group');
            if (servicesContainer) {
                let errorElement = servicesContainer.parentElement.querySelector('.form-error');
                if (!errorElement) {
                    errorElement = document.createElement('div');
                    errorElement.className = 'form-error visible';
                    servicesContainer.parentElement.appendChild(errorElement);
                }
                errorElement.textContent = 'Please select at least one service';
                errorElement.classList.add('visible');
            }
        }

        return isValid;
    }

    handleSubmit(e) {
        if (!this.validateForm()) {
            e.preventDefault();

            // Scroll to first error
            const firstError = this.form.querySelector('.error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            showAlert('Please fix the errors before submitting', 'error');
            return false;
        }

        // Show loading state
        const submitBtn = this.form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner"></span> Generating Contract...';
        }

        return true;
    }
}

// Progress Steps
class ProgressSteps {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentStep = 1;
        this.totalSteps = 3;
        this.init();
    }

    init() {
        if (!this.container) return;
        this.updateProgress();
    }

    setStep(step) {
        this.currentStep = step;
        this.updateProgress();
    }

    updateProgress() {
        const steps = this.container.querySelectorAll('.step');
        const progressLine = this.container.querySelector('.progress-line');

        steps.forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');

            if (stepNum < this.currentStep) {
                step.classList.add('completed');
            } else if (stepNum === this.currentStep) {
                step.classList.add('active');
            }
        });

        // Update progress line
        if (progressLine) {
            const progress = ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
            progressLine.style.width = `${progress}%`;
        }
    }

    next() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateProgress();
        }
    }

    prev() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateProgress();
        }
    }
}

// Modal Management
class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        this.init();
    }

    init() {
        if (!this.modal) return;

        // Close on backdrop click
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        // Close on close button click
        const closeBtn = this.modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close());
        }

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.close();
            }
        });
    }

    open() {
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    setContent(title, body) {
        const modalTitle = this.modal.querySelector('.modal-title');
        const modalBody = this.modal.querySelector('.modal-body');

        if (modalTitle) modalTitle.textContent = title;
        if (modalBody) modalBody.innerHTML = body;
    }
}

// Alert System
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
    <span>${getAlertIcon(type)}</span>
    <span>${message}</span>
  `;

    alertContainer.appendChild(alert);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

function getAlertIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

// Checkbox Group Enhancement
function initCheckboxGroups() {
    const checkboxItems = document.querySelectorAll('.checkbox-item');

    checkboxItems.forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');

        if (checkbox) {
            // Update visual state
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    item.classList.add('checked');
                } else {
                    item.classList.remove('checked');
                }
            });

            // Make entire item clickable
            item.addEventListener('click', (e) => {
                if (e.target !== checkbox) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}

// Fee Input Formatting
function initFeeFormatting() {
    const feeInput = document.querySelector('input[name="fees"]');

    if (feeInput) {
        feeInput.addEventListener('input', (e) => {
            let value = e.target.value.replace(/,/g, '');

            if (!isNaN(value) && value !== '') {
                // Format with commas
                const formatted = parseFloat(value).toLocaleString('en-US', {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 2
                });
                e.target.value = formatted;
            }
        });
    }
}

// Currency Converter Display
function initCurrencyConverter() {
    const feeInput = document.querySelector('input[name="fees"]');
    const currencySelect = document.querySelector('select[name="currency"]');
    const converterDisplay = document.getElementById('currencyConverter');

    if (!feeInput || !currencySelect || !converterDisplay) return;

    const rates = {
        USD: { symbol: '$', name: 'US Dollars', rate: 1 },
        EUR: { symbol: '€', name: 'Euros', rate: 1.08 },
        GBP: { symbol: '£', name: 'Pounds Sterling', rate: 1.27 },
        AED: { symbol: 'AED ', name: 'UAE Dirhams', rate: 0.27 },
        SAR: { symbol: 'SAR ', name: 'Saudi Riyals', rate: 0.27 },
        BHD: { symbol: 'BHD ', name: 'Bahraini Dinars', rate: 2.65 },
        QAR: { symbol: 'QAR ', name: 'Qatari Riyals', rate: 0.27 },
        KWD: { symbol: 'KWD ', name: 'Kuwaiti Dinars', rate: 3.25 },
        OMR: { symbol: 'OMR ', name: 'Omani Riyals', rate: 2.60 },
        PKR: { symbol: 'PKR ', name: 'Pakistani Rupees', rate: 0.0036 }
    };

    function updateConverter() {
        const amount = parseFloat(feeInput.value.replace(/,/g, '')) || 0;
        const currency = currencySelect.value;
        const currencyData = rates[currency];

        if (amount > 0 && currencyData) {
            const usdEquivalent = amount * currencyData.rate;
            converterDisplay.innerHTML = `
        <div class="alert alert-info">
          <span>💱</span>
          <span>
            <strong>${currencyData.symbol}${amount.toLocaleString()}</strong> 
            = approximately 
            <strong>$${usdEquivalent.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USD</strong>
          </span>
        </div>
      `;
        } else {
            converterDisplay.innerHTML = '';
        }
    }

    feeInput.addEventListener('input', updateConverter);
    currencySelect.addEventListener('change', updateConverter);
}

// Contract Preview
async function showContractPreview() {
    const form = document.getElementById('contractForm');
    if (!form) return;

    const formData = new FormData(form);
    const data = {
        client_name: formData.get('client_name'),
        country: formData.get('country'),
        fees: formData.get('fees'),
        currency: formData.get('currency'),
        duration: formData.get('duration'),
        services: formData.getAll('services')
    };

    const previewContent = `
    <div class="card">
      <h3>Contract Summary</h3>
      <table>
        <tr>
          <td><strong>Client Name:</strong></td>
          <td>${data.client_name}</td>
        </tr>
        <tr>
          <td><strong>Country:</strong></td>
          <td>${data.country}</td>
        </tr>
        <tr>
          <td><strong>Contract Duration:</strong></td>
          <td>${data.duration}</td>
        </tr>
        <tr>
          <td><strong>Fee Amount:</strong></td>
          <td>${data.fees} ${data.currency}</td>
        </tr>
        <tr>
          <td><strong>Services:</strong></td>
          <td>${data.services.map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(', ')}</td>
        </tr>
      </table>
    </div>
    <div class="alert alert-info mt-2">
      <span>ℹ</span>
      <span>Please review the details above. Click "Generate Contract" to create your professional service agreement.</span>
    </div>
  `;

    const modal = new Modal('previewModal');
    modal.setContent('Contract Preview', previewContent);
    modal.open();
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme
    initTheme();
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Initialize form validation
    const validator = new FormValidator('contractForm');

    // Initialize checkbox groups
    initCheckboxGroups();

    // Initialize fee formatting
    initFeeFormatting();

    // Initialize currency converter
    initCurrencyConverter();

    // Preview button
    const previewBtn = document.getElementById('previewBtn');
    if (previewBtn) {
        previewBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const form = document.getElementById('contractForm');
            const validator = new FormValidator('contractForm');

            if (validator.validateForm()) {
                showContractPreview();
            } else {
                showAlert('Please fix the errors before previewing', 'error');
            }
        });
    }
});

// Export for use in other scripts
window.ContractGenerator = {
    FormValidator,
    ProgressSteps,
    Modal,
    showAlert
};
