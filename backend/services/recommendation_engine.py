import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.models import Product, Interaction, get_db
from config.settings import MAX_RECOMMENDATIONS, MIN_SCORE_THRESHOLD


class HybridRecommendationEngine:
    """
    Hybrid Recommendation System combining:
    1. Rule-Based Filtering (Phase 1)
    2. Collaborative Filtering (Phase 2 - ML)
    3. Content-Based Filtering (Phase 2 - ML)
    """
    
    def __init__(self):
        self.db = get_db()
        self.scaler = MinMaxScaler()
    
    def get_recommendations(self, user_preferences, use_ml=False):
        """
        Main recommendation method
        
        Args:
            user_preferences: dict with budget_min, budget_max, metal_type, occasion, style, category
            use_ml: bool - whether to use ML-based recommendations (default: False for Phase 1)
        
        Returns:
            list of recommended products
        """
        if use_ml and self._has_sufficient_data():
            # Phase 2: Hybrid approach (Rule-based + ML)
            rule_based_products = self._rule_based_filter(user_preferences)
            ml_products = self._ml_based_recommendations(user_preferences)
            return self._merge_recommendations(rule_based_products, ml_products)
        else:
            # Phase 1: Pure rule-based
            return self._rule_based_filter(user_preferences)
    
    def _rule_based_filter(self, preferences):
        """
        Rule-based recommendation using exact matching and scoring
        """
        query = self.db.query(Product)
        
        # Filter by budget
        if preferences.get('budget_min') and preferences.get('budget_max'):
            query = query.filter(
                Product.price >= preferences['budget_min'],
                Product.price <= preferences['budget_max']
            )
        
        # Get all matching products
        products = query.all()
        
        # Score each product
        scored_products = []
        for product in products:
            score = self._calculate_rule_score(product, preferences)
            if score >= MIN_SCORE_THRESHOLD:
                scored_products.append({
                    'product': product,
                    'score': score
                })
        
        # Sort by score and return top N
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        return [item['product'] for item in scored_products[:MAX_RECOMMENDATIONS]]
    
    def _calculate_rule_score(self, product, preferences):
        """
        Calculate score for a product based on user preferences
        
        Scoring logic:
        - Exact metal match: +30 points
        - Exact occasion match: +25 points
        - Exact style match: +20 points
        - Exact category match: +15 points
        - Popularity bonus: +10 points (normalized)
        - Price within range: already filtered
        """
        score = 0.0
        
        # Metal type match
        if preferences.get('metal_type') and product.metal_type == preferences['metal_type']:
            score += 30
        
        # Occasion match
        if preferences.get('occasion') and product.occasion == preferences['occasion']:
            score += 25
        
        # Style match
        if preferences.get('style') and product.style == preferences['style']:
            score += 20
        
        # Category match
        if preferences.get('category') and product.category == preferences['category']:
            score += 15
        
        # Popularity bonus (normalized 0-10)
        if product.popularity:
            score += (product.popularity / 100) * 10
        
        # Normalize to 0-1 range
        return score / 100.0
    
    def _ml_based_recommendations(self, preferences):
        """
        ML-based recommendations using collaborative filtering
        (Phase 2 - requires interaction data)
        """
        # Get user-item interaction matrix
        interaction_matrix = self._build_interaction_matrix()
        
        if interaction_matrix is None:
            return []
        
        # Calculate product similarities using cosine similarity
        product_similarities = cosine_similarity(interaction_matrix)
        
        # Get products based on similar user interactions
        # This is a simplified version - full implementation would use matrix factorization
        recommended_products = self._get_similar_products(product_similarities, preferences)
        
        return recommended_products
    
    def _build_interaction_matrix(self):
        """
        Build user-item interaction matrix from interaction logs
        Returns None if insufficient data
        """
        interactions = self.db.query(Interaction).all()
        
        if len(interactions) < 50:  # Need minimum interactions for ML
            return None
        
        # Build matrix (simplified - in production use sparse matrix)
        # This would be implemented with pandas pivot table or scipy sparse matrix
        return None  # Placeholder for Phase 2
    
    def _get_similar_products(self, similarity_matrix, preferences):
        """
        Get products similar to user preferences using similarity matrix
        """
        # Placeholder for Phase 2 ML implementation
        return []
    
    def _merge_recommendations(self, rule_based, ml_based):
        """
        Merge rule-based and ML-based recommendations
        Weighted combination: 60% rule-based, 40% ML-based
        """
        merged = []
        seen_ids = set()
        
        # Add rule-based (60%)
        for i, product in enumerate(rule_based):
            if i < int(MAX_RECOMMENDATIONS * 0.6):
                if product.id not in seen_ids:
                    merged.append(product)
                    seen_ids.add(product.id)
        
        # Add ML-based (40%)
        for product in ml_based:
            if len(merged) >= MAX_RECOMMENDATIONS:
                break
            if product.id not in seen_ids:
                merged.append(product)
                seen_ids.add(product.id)
        
        return merged[:MAX_RECOMMENDATIONS]
    
    def _has_sufficient_data(self):
        """
        Check if we have enough interaction data for ML recommendations
        """
        interaction_count = self.db.query(Interaction).count()
        return interaction_count >= 100  # Minimum threshold for ML
    
    def track_interaction(self, session_id, product_id, action_type):
        """
        Track user interaction for future ML model training
        """
        interaction = Interaction(
            session_id=session_id,
            product_id=product_id,
            action_type=action_type
        )
        self.db.add(interaction)
        self.db.commit()
        
        # Update product popularity
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.popularity = min(100, product.popularity + 1)
            self.db.commit()
    
    def get_trending_products(self, limit=10):
        """
        Get trending products based on popularity
        """
        products = self.db.query(Product).order_by(Product.popularity.desc()).limit(limit).all()
        return products
    
    def close(self):
        """Close database session"""
        self.db.close()


# Convenience function
def get_recommendations(user_preferences, use_ml=False):
    """
    Get product recommendations based on user preferences
    
    Args:
        user_preferences: dict with budget_min, budget_max, metal_type, occasion, style, category
        use_ml: bool - whether to use ML (default False for Phase 1)
    
    Returns:
        list of Product objects
    """
    engine = HybridRecommendationEngine()
    try:
        recommendations = engine.get_recommendations(user_preferences, use_ml)
        return recommendations
    finally:
        engine.close()
