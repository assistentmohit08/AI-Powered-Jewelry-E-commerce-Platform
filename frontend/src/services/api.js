// src/services/api.js
import axios from 'axios';

/**
 * Base URL for the API.
 * Defaults to localhost:5000 if not specified in environment variables.
 */
// Automatically append /api/chatbot if not present
let API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'https://jewelry-api.onrender.com/api/chatbot';
if (API_BASE_URL && !API_BASE_URL.endsWith('/api/chatbot')) {
    API_BASE_URL += '/api/chatbot';
}

console.log("🔌 API Base URL:", API_BASE_URL); // Debugging log

/**
 * Axios instance with default configuration.
 */
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a response interceptor for global error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API Call Failed:", error.response ? error.response.data : error.message);
        // You could add logic here to handle 401 Unauthorized globally etc.
        return Promise.reject(error);
    }
);

/**
 * Service object for handling all Chatbot related API calls.
 */
export const chatbotAPI = {
    /**
     * Starts a new chat session.
     * @returns {Promise<Object>} The response data containing session_id and welcome message.
     */
    startSession: async () => {
        try {
            const response = await api.post('/start');
            return response.data;
        } catch (error) {
            console.error('Error starting session:', error);
            throw error;
        }
    },

    /**
     * Sends a message to the chatbot.
     * @param {string} sessionId - The current session ID.
     * @param {string} message - The message text to send.
     * @returns {Promise<Object>} The response data containing the bot's reply.
     */
    sendMessage: async (sessionId, message) => {
        try {
            const response = await api.post('/message', {
                session_id: sessionId,
                message: message,
            });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    },

    /**
     * Tracks user interaction with a product.
     * @param {string} sessionId - The current session ID.
     * @param {string|number} productId - The ID of the product interacted with.
     * @param {string} actionType - The type of action (e.g., 'click', 'view').
     * @returns {Promise<Object>} The tracking response.
     */
    trackInteraction: async (sessionId, productId, actionType) => {
        try {
            const response = await api.post('/track', {
                session_id: sessionId,
                product_id: productId,
                action_type: actionType,
            });
            return response.data;
        } catch (error) {
            console.error('Error tracking interaction:', error);
            throw error;
        }
    },

    /**
     * Fetches trending products.
     * @param {number} [limit=6] - The maximum number of products to return.
     * @returns {Promise<Object>} The response data containing trending products.
     */
    getTrendingProducts: async (limit = 6) => {
        try {
            const response = await api.get(`/trending?limit=${limit}`);
            return response.data;
        } catch (error) {
            console.error('Error getting trending products:', error);
            throw error;
        }
    },
};

export default api;