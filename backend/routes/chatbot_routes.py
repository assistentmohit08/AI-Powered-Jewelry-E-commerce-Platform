from flask import Blueprint, request, jsonify
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.services.chatbot_service import ChatbotService
from backend.services.recommendation_engine import HybridRecommendationEngine

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/start', methods=['POST'])
def start_chatbot():
    """
    Initialize a new chatbot session
    
    Returns:
        {
            "session_id": "uuid",
            "message": "Welcome message",
            "options": ["option1", "option2", ...]
        }
    """
    try:
        chatbot = ChatbotService()
        response = chatbot.start_session()
        chatbot.close()
        
        return jsonify({
            'success': True,
            'data': response
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@chatbot_bp.route('/message', methods=['POST'])
def process_message():
    """
    Process user message and return bot response
    
    Request body:
        {
            "session_id": "uuid",
            "message": "user message"
        }
    
    Returns:
        {
            "message": "bot response",
            "options": ["option1", "option2", ...],
            "conversation_state": "state",
            "products": [...] (if recommendations ready)
        }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        user_message = data.get('message')
        
        if not session_id or not user_message:
            return jsonify({
                'success': False,
                'error': 'session_id and message are required'
            }), 400
        
        # Process message
        chatbot = ChatbotService()
        response = chatbot.process_message(session_id, user_message)
        
        # If ready for recommendations, get them
        if response.get('ready_for_recommendations'):
            preferences = chatbot.get_session_preferences(session_id)
            
            # Get recommendations from hybrid engine
            rec_engine = HybridRecommendationEngine()
            products = rec_engine.get_recommendations(preferences, use_ml=False)
            rec_engine.close()
            
            # Add products to response
            response['products'] = [p.to_dict() for p in products]
            response['message'] = f"Here are {len(products)} perfect matches for you! 💎✨"
        
        chatbot.close()
        
        return jsonify({
            'success': True,
            'data': response
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@chatbot_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """
    Get conversation history for a session
    
    Returns:
        {
            "history": [
                {"message": "...", "sender": "user/bot", "timestamp": "..."},
                ...
            ]
        }
    """
    try:
        chatbot = ChatbotService()
        history = chatbot.get_conversation_history(session_id)
        chatbot.close()
        
        return jsonify({
            'success': True,
            'data': {'history': history}
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@chatbot_bp.route('/track', methods=['POST'])
def track_interaction():
    """
    Track user interaction with products
    
    Request body:
        {
            "session_id": "uuid",
            "product_id": 123,
            "action_type": "view/click/like"
        }
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        product_id = data.get('product_id')
        action_type = data.get('action_type', 'view')
        
        if not session_id or not product_id:
            return jsonify({
                'success': False,
                'error': 'session_id and product_id are required'
            }), 400
        
        # Track interaction
        rec_engine = HybridRecommendationEngine()
        rec_engine.track_interaction(session_id, product_id, action_type)
        rec_engine.close()
        
        return jsonify({
            'success': True,
            'message': 'Interaction tracked successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@chatbot_bp.route('/trending', methods=['GET'])
def get_trending():
    """
    Get trending products
    
    Returns:
        {
            "products": [...]
        }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        rec_engine = HybridRecommendationEngine()
        products = rec_engine.get_trending_products(limit)
        rec_engine.close()
        
        return jsonify({
            'success': True,
            'data': {
                'products': [p.to_dict() for p in products]
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
