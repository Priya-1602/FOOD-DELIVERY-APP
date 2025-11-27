
let cart = {};
let searchTimeout;

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    loadCartFromStorage();
    initializeEventListeners();
    initializeTooltips();
    initializeFormValidations();
}

function addToCart(itemId, quantity = 1) {
    if (cart[itemId]) {
        cart[itemId] += quantity;
    } else {
        cart[itemId] = quantity;
    }
    
    saveCartToStorage();
    updateCartBadge();
    showToast('Item added to cart!', 'success');
}

function removeFromCart(itemId) {
    delete cart[itemId];
    saveCartToStorage();
    updateCartBadge();
    showToast('Item removed from cart!', 'info');
}

function updateCartQuantity(itemId, quantity) {
    if (quantity <= 0) {
        removeFromCart(itemId);
    } else {
        cart[itemId] = quantity;
        saveCartToStorage();
        updateCartBadge();
    }
}

function clearCart() {
    cart = {};
    saveCartToStorage();
    updateCartBadge();
    showToast('Cart cleared!', 'info');
}

function getCartTotal() {
    let total = 0;
    for (let itemId in cart) {
        const item = getMenuItemById(itemId);
        if (item) {
            total += item.price * cart[itemId];
        }
    }
    return total;
}

function getCartItemCount() {
    let count = 0;
    for (let itemId in cart) {
        count += cart[itemId];
    }
    return count;
}

// Storage functions
function saveCartToStorage() {
    sessionStorage.setItem('cart', JSON.stringify(cart));
}

function loadCartFromStorage() {
    const savedCart = sessionStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartBadge();
    }
}

function updateCartBadge() {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        const count = getCartItemCount();
        cartBadge.textContent = count;
        cartBadge.style.display = count > 0 ? 'inline' : 'none';
    }
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-custom show bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} text-white`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 250px;
    `;
    
    toast.innerHTML = `
        <div class="toast-body">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            ${message}
        </div>
    `;
    
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

function performSearch(query) {
    const menuItems = document.querySelectorAll('.menu-item-card');
    const queryLower = query.toLowerCase();
    
    menuItems.forEach(item => {
        const name = item.dataset.name || '';
        const description = item.dataset.description || '';
        
        if (name.includes(queryLower) || description.includes(queryLower)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
    
    // Show/hide no results message
    const visibleItems = document.querySelectorAll('.menu-item-card[style="display: block"]');
    const noResults = document.getElementById('noResults');
    if (noResults) {
        noResults.style.display = visibleItems.length === 0 ? 'block' : 'none';
    }
}

// Form validation functions
function initializeFormValidations() {
    // Registration form validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', validateRegistrationForm);
    }
    
    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', validateLoginForm);
    }
    
    // Checkout form validation
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', validateCheckoutForm);
    }
}

function validateRegistrationForm(e) {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const email = document.getElementById('email');
    
    // Email validation
    if (!isValidEmail(email.value)) {
        e.preventDefault();
        showToast('Please enter a valid email address!', 'error');
        return false;
    }
    
    // Password validation
    if (password.value.length < 8) {
        e.preventDefault();
        showToast('Password must be at least 8 characters long!', 'error');
        return false;
    }
    
    // Password confirmation
    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        showToast('Passwords do not match!', 'error');
        return false;
    }
    
    return true;
}

function validateLoginForm(e) {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    
    if (!email.value || !password.value) {
        e.preventDefault();
        showToast('Please fill in all fields!', 'error');
        return false;
    }
    
    return true;
}

function validateCheckoutForm(e) {
    const deliveryAddress = document.getElementById('delivery_address');
    const termsAgree = document.getElementById('terms_agree');
    
    if (!deliveryAddress.value.trim()) {
        e.preventDefault();
        showToast('Please enter a delivery address!', 'error');
        return false;
    }
    
    if (!termsAgree.checked) {
        e.preventDefault();
        showToast('Please agree to the terms and conditions!', 'error');
        return false;
    }
    
    return true;
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getMenuItemById(itemId) {
    // This would typically fetch from an API
    // For now, return a mock item
    return {
        id: itemId,
        name: 'Sample Item',
        price: 10.99
    };
}

// Event listeners
function initializeEventListeners() {
    // Initialize search
    initializeSearch();
    
    // Initialize password strength checker
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
    
    // Initialize password confirmation checker
    const confirmPasswordInput = document.getElementById('confirm_password');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            checkPasswordMatch();
        });
    }
    
    // Initialize quantity controls
    initializeQuantityControls();
    
    // Initialize payment method toggles
    initializePaymentToggles();
}

function initializeQuantityControls() {
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const value = parseInt(this.value);
            if (value < 0) this.value = 0;
            if (value > 10) this.value = 10;
        });
    });
}

function initializePaymentToggles() {
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    const cardDetails = document.getElementById('cardDetails');
    
    if (paymentMethods.length && cardDetails) {
        paymentMethods.forEach(method => {
            method.addEventListener('change', function() {
                if (this.value === 'card') {
                    cardDetails.style.display = 'block';
                } else {
                    cardDetails.style.display = 'none';
                }
            });
        });
    }
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    const feedback = [];
    
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('Lowercase letter');
    
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('Uppercase letter');
    
    if (/[0-9]/.test(password)) strength++;
    else feedback.push('Number');
    
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    else feedback.push('Special character');
    
    const strengthBar = document.getElementById('password-strength');
    if (strengthBar) {
        strengthBar.className = 'password-strength';
        
        if (strength <= 2) {
            strengthBar.classList.add('strength-weak');
        } else if (strength <= 3) {
            strengthBar.classList.add('strength-medium');
        } else {
            strengthBar.classList.add('strength-strong');
        }
    }
    
    return { strength, feedback };
}

function checkPasswordMatch() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const passwordMatch = document.getElementById('password-match');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!password || !confirmPassword || !passwordMatch) return;
    
    if (confirmPassword.value === '') {
        passwordMatch.innerHTML = '';
        return;
    }
    
    if (password.value === confirmPassword.value) {
        passwordMatch.innerHTML = '<small class="text-success"><i class="fas fa-check"></i> Passwords match</small>';
        if (submitBtn) submitBtn.disabled = false;
    } else {
        passwordMatch.innerHTML = '<small class="text-danger"><i class="fas fa-times"></i> Passwords do not match</small>';
        if (submitBtn) submitBtn.disabled = true;
    }
}

// Auto-refresh functions
function startAutoRefresh() {
    // Auto-refresh cart badge
    setInterval(() => {
        updateCartBadge();
    }, 5000);
    
    // Auto-refresh order status (if on order page)
    if (window.location.pathname.includes('order')) {
        setInterval(() => {
            refreshOrderStatus();
        }, 30000);
    }
}

function refreshOrderStatus() {
    // This would typically make an AJAX call to check for status updates
    console.log('Refreshing order status...');
}

// Export functions for global access
window.RestaurantApp = {
    addToCart,
    removeFromCart,
    updateCartQuantity,
    clearCart,
    getCartTotal,
    getCartItemCount,
    showToast,
    formatPrice,
    formatDate,
    checkPasswordStrength,
    checkPasswordMatch
};

// Start auto-refresh
startAutoRefresh(); 