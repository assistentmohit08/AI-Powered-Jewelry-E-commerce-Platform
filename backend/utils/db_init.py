import json
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from backend.models import Product, init_db, get_db

def load_sample_products():
    """Load sample products from JSON file into database"""
    
    # Initialize database
    init_db()
    
    # Get database session
    db = get_db()
    
    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} products. Skipping import.")
        db.close()
        return
    
    # Load JSON file
    json_path = os.path.join(project_root, 'data', 'sample_products.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        products_data = json.load(f)
    
    # Insert products
    for product_data in products_data:
        product = Product(
            name=product_data['name'],
            category=product_data['category'],
            metal_type=product_data['metal_type'],
            price=product_data['price'],
            occasion=product_data['occasion'],
            style=product_data['style'],
            image_url=product_data['image_url'],
            description=product_data['description'],
            popularity=product_data.get('popularity', 50)
        )
        db.add(product)
    
    db.commit()
    print(f"✅ Successfully loaded {len(products_data)} products into database!")
    
    db.close()

if __name__ == '__main__':
    print("🔄 Loading sample products into database...")
    load_sample_products()
    print("✨ Database initialization complete!")

