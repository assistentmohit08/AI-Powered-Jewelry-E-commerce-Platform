from flask import Flask
from flask_cors import CORS
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import SECRET_KEY, DEBUG, CORS_ORIGINS
from backend.models import init_db, get_db, Product
from backend.routes.chatbot_routes import chatbot_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

# Register blueprints
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

# Initialize database and load sample products
with app.app_context():
    init_db()
    print("✅ Database initialized successfully!")
    
    # Load sample products
    db = get_db()
    
    # Check if products already exist
    existing_count = db.query(Product).count()
    
    if existing_count == 0:
        print("📦 Loading sample products...")
        
        # Load sample products from JSON
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        products_file = os.path.join(base_path, 'data', 'sample_products.json')
        
        try:
            with open(products_file, 'r') as f:
                products_data = json.load(f)
            
            for product_data in products_data:
                product = Product(
                    name=product_data.get('name'),
                    category=product_data.get('category'),
                    metal_type=product_data.get('metal_type'),
                    price=product_data.get('price'),
                    occasion=product_data.get('occasion'),
                    style=product_data.get('style'),
                    image_url=product_data.get('image_url'),
                    description=product_data.get('description'),
                    popularity=product_data.get('popularity', 0)
                )
                db.add(product)
            
            db.commit()
            print(f"✅ Loaded {len(products_data)} sample products!")
        except Exception as e:
            print(f"⚠️  Could not load sample products: {e}")
        finally:
            db.close()
    else:
        print(f"📦 Database has {existing_count} products already!")


@app.route('/')
def index():
    """Health check endpoint"""
    return {
        'status': 'running',
        'message': 'Jewelry Recommendation Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'chatbot_start': '/api/chatbot/start',
            'chatbot_message': '/api/chatbot/message',
            'chatbot_history': '/api/chatbot/history/<session_id>',
            'track_interaction': '/api/chatbot/track',
            'trending_products': '/api/chatbot/trending'
        }
    }


@app.route('/health')
def health():
    """Health check"""
    return {'status': 'healthy'}, 200


if __name__ == '__main__':
    print("🚀 Starting Jewelry Recommendation Chatbot API...")
    print("📍 Server running on http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
