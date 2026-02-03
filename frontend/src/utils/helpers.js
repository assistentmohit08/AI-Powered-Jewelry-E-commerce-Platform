// src/utils/helpers.js

// Format price in Indian Rupees
export const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0,
    }).format(price);
};

// Escape HTML to prevent XSS
export const escapeHtml = (text) => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

// Session storage helpers
export const sessionStorage = {
    save: (sessionId) => {
        if (sessionId) {
            localStorage.setItem('chatbot_session_id', sessionId);
        }
    },

    load: () => {
        return localStorage.getItem('chatbot_session_id');
    },

    clear: () => {
        localStorage.removeItem('chatbot_session_id');
    },
};

// Scroll to bottom smoothly
export const scrollToBottom = (element) => {
    if (element) {
        setTimeout(() => {
            element.scrollTop = element.scrollHeight;
        }, 100);
    }
};