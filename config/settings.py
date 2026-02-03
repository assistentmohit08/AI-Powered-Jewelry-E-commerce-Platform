import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'ecommerce.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask configuration
SECRET_KEY = 'your-secret-key-change-in-production'
DEBUG = True

# CORS configuration
CORS_ORIGINS = [
    # Frontend servers
    'http://localhost:8000',        # Python HTTP server (RECOMMENDED)
    'http://127.0.0.1:8000',
    'http://localhost:5500',        # VS Code Live Server
    'http://127.0.0.1:5500',
    
    # Backend
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    
    # Vercel Frontend
    'https://ai-powered-jewelry-e-commerce-platf.vercel.app',
    
    # Allow all for development (remove in production!)
    '*'
]

# Recommendation engine settings
MAX_RECOMMENDATIONS = 10
MIN_SCORE_THRESHOLD = 0.3

# Chatbot configuration
CONVERSATION_STATES = [
    'started',
    'asking_budget',
    'asking_metal',
    'asking_occasion',
    'asking_style',
    'asking_category',
    'showing_recommendations',
    'completed'
]

# Budget ranges
BUDGET_RANGES = {
    'under_10k': (0, 10000),
    '10k_25k': (10000, 25000),
    '25k_50k': (25000, 50000),
    '50k_plus': (50000, 1000000)
}

# Valid options
METAL_TYPES = ['Gold', 'Silver', 'Platinum', 'Diamond', 'Rose Gold']
OCCASIONS = ['Wedding', 'Anniversary', 'Birthday', 'Daily Wear', 'Gift', 'Engagement', 'Festival']
STYLES = ['Traditional', 'Modern', 'Minimalist', 'Vintage', 'Contemporary']
CATEGORIES = ['Rings', 'Necklaces', 'Earrings', 'Bracelets', 'Bangles', 'Pendants', 'Chains']
