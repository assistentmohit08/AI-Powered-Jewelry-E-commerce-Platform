import re
import uuid
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.models import UserSession, ConversationHistory, get_db
from config.settings import BUDGET_RANGES, METAL_TYPES, OCCASIONS, STYLES, CATEGORIES


class ChatbotService:
    """
    Chatbot conversation flow manager
    Handles question sequencing, user input parsing, and state management
    """
    
    def __init__(self):
        self.db = get_db()
        self.conversation_flow = [
            'asking_metal',
            'asking_budget',
            'asking_occasion',
            'asking_style',
            'asking_category',
            'showing_recommendations'
        ]
    
    def start_session(self):
        """
        Start a new chatbot session
        Returns: session_id and welcome message
        """
        session_id = str(uuid.uuid4())
        
        # Create new session
        session = UserSession(
            session_id=session_id,
            conversation_state='started'
        )
        self.db.add(session)
        self.db.commit()
        
        # Add welcome message to history
        welcome_message = "Hi! 👋 I'm your jewelry shopping assistant. I'll help you find the perfect piece! To get started, what metal type do you prefer?"
        self._add_to_history(session_id, welcome_message, 'bot')
        
        # Update state
        self._update_session_state(session_id, 'asking_metal')
        
        return {
            'session_id': session_id,
            'message': welcome_message,
            'options': METAL_TYPES
        }
    
    def process_message(self, session_id, user_message):
        """
        Process user message and return bot response
        
        Args:
            session_id: str
            user_message: str
        
        Returns:
            dict with bot_message, options, and conversation_state
        """
        # Get session
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if not session:
            return self.start_session()
        
        # Check for global restart commands
        if user_message.lower().strip() in ['start', 'restart', 'reset']:
            # Force start a new session
            return self.start_session()
        
        # Add user message to history
        self._add_to_history(session_id, user_message, 'user')
        
        # Process based on current state
        current_state = session.conversation_state
        
        if current_state == 'started' or current_state == 'asking_metal':
            return self._handle_metal(session, user_message)
        
        elif current_state == 'asking_budget':
            return self._handle_budget(session, user_message)
        
        elif current_state == 'asking_occasion':
            return self._handle_occasion(session, user_message)
        
        elif current_state == 'asking_style':
            return self._handle_style(session, user_message)
        
        elif current_state == 'asking_category':
            return self._handle_category(session, user_message)
        
        else:
            # Default response
            return {
                'message': "I'm not sure I understand. Let's start over!",
                'options': [],
                'conversation_state': current_state
            }
    
    def _handle_budget(self, session, user_message):
        """Handle budget input"""
        budget_min, budget_max = self._parse_budget(user_message)
        
        if budget_min is None:
            return {
                'message': "I didn't quite catch that. Please select your budget range:",
                'options': [
                    'Under ₹10,000',
                    '₹10,000 - ₹25,000',
                    '₹25,000 - ₹50,000',
                    '₹50,000+'
                ],
                'conversation_state': 'asking_budget'
            }
        
        # Update session
        session.budget_min = budget_min
        session.budget_max = budget_max
        self._update_session_state(session.session_id, 'asking_occasion')
        
        message = f"Great! Budget set to ₹{int(budget_min):,} - ₹{int(budget_max):,}. What's the occasion?"
        self._add_to_history(session.session_id, message, 'bot')
        
        return {
            'message': message,
            'options': OCCASIONS,
            'conversation_state': 'asking_occasion'
        }
    
    def _handle_metal(self, session, user_message):
        """Handle metal type input"""
        metal = self._parse_option(user_message, METAL_TYPES)
        
        if not metal:
            return {
                'message': "Please select a metal type:",
                'options': METAL_TYPES,
                'conversation_state': 'asking_metal'
            }
        
        session.metal_type = metal
        self._update_session_state(session.session_id, 'asking_budget')
        
        message = f"Perfect! {metal} is a great choice. What's your budget range?"
        self._add_to_history(session.session_id, message, 'bot')
        
        return {
            'message': message,
            'options': [
                'Under ₹10,000',
                '₹10,000 - ₹25,000',
                '₹25,000 - ₹50,000',
                '₹50,000+'
            ],
            'conversation_state': 'asking_budget'
        }
    
    def _handle_occasion(self, session, user_message):
        """Handle occasion input"""
        occasion = self._parse_option(user_message, OCCASIONS)
        
        if not occasion:
            return {
                'message': "Please select an occasion:",
                'options': OCCASIONS,
                'conversation_state': 'asking_occasion'
            }
        
        session.occasion = occasion
        self._update_session_state(session.session_id, 'asking_style')
        
        message = f"Lovely! {occasion} is special. What style do you prefer?"
        self._add_to_history(session.session_id, message, 'bot')
        
        return {
            'message': message,
            'options': STYLES,
            'conversation_state': 'asking_style'
        }
    
    def _handle_style(self, session, user_message):
        """Handle style input"""
        style = self._parse_option(user_message, STYLES)
        
        if not style:
            return {
                'message': "Please select a style:",
                'options': STYLES,
                'conversation_state': 'asking_style'
            }
        
        session.style = style
        self._update_session_state(session.session_id, 'asking_category')
        
        message = f"Excellent! {style} style it is. What category are you looking for?"
        self._add_to_history(session.session_id, message, 'bot')
        
        return {
            'message': message,
            'options': CATEGORIES,
            'conversation_state': 'asking_category'
        }
    
    def _handle_category(self, session, user_message):
        """Handle category input and trigger recommendations"""
        category = self._parse_option(user_message, CATEGORIES)
        
        if not category:
            return {
                'message': "Please select a category:",
                'options': CATEGORIES,
                'conversation_state': 'asking_category'
            }
        
        session.category = category
        self._update_session_state(session.session_id, 'showing_recommendations')
        
        message = f"Perfect! Let me find the best {category.lower()} for you... 💎"
        self._add_to_history(session.session_id, message, 'bot')
        
        return {
            'message': message,
            'options': [],
            'conversation_state': 'showing_recommendations',
            'ready_for_recommendations': True
        }
    
    def _parse_budget(self, user_input):
        """
        Parse budget from user input
        Returns: (budget_min, budget_max) or (None, None)
        """
        user_input = user_input.lower()
        
        # Check for predefined ranges
        if 'under' in user_input or '10000' in user_input or '10k' in user_input:
            if 'under' in user_input or ('10' in user_input and 'under' in user_input):
                return BUDGET_RANGES['under_10k']
        
        if ('10' in user_input and '25' in user_input) or ('10k' in user_input and '25k' in user_input):
            return BUDGET_RANGES['10k_25k']
        
        if ('25' in user_input and '50' in user_input) or ('25k' in user_input and '50k' in user_input):
            return BUDGET_RANGES['25k_50k']
        
        if '50' in user_input or '50k' in user_input or 'above' in user_input or 'plus' in user_input:
            return BUDGET_RANGES['50k_plus']
        
        # Try to extract numbers
        numbers = re.findall(r'\d+', user_input)
        if len(numbers) >= 2:
            return (float(numbers[0]), float(numbers[1]))
        elif len(numbers) == 1:
            num = float(numbers[0])
            if num < 10000:
                return BUDGET_RANGES['under_10k']
            elif num < 25000:
                return BUDGET_RANGES['10k_25k']
            elif num < 50000:
                return BUDGET_RANGES['25k_50k']
            else:
                return BUDGET_RANGES['50k_plus']
        
        return (None, None)
    
    def _parse_option(self, user_input, valid_options):
        """
        Parse user input against valid options
        Returns: matched option or None
        """
        user_input = user_input.lower().strip()
        
        for option in valid_options:
            if option.lower() in user_input or user_input in option.lower():
                return option
        
        return None
    
    def _add_to_history(self, session_id, message, sender):
        """Add message to conversation history"""
        history = ConversationHistory(
            session_id=session_id,
            message=message,
            sender=sender
        )
        self.db.add(history)
        self.db.commit()
    
    def _update_session_state(self, session_id, new_state):
        """Update session conversation state"""
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if session:
            session.conversation_state = new_state
            session.updated_at = datetime.utcnow()
            self.db.commit()
    
    def get_session_preferences(self, session_id):
        """
        Get user preferences from session
        Returns: dict with all preferences
        """
        session = self.db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()
        
        if not session:
            return None
        
        return {
            'budget_min': session.budget_min,
            'budget_max': session.budget_max,
            'metal_type': session.metal_type,
            'occasion': session.occasion,
            'style': session.style,
            'category': session.category
        }
    
    def get_conversation_history(self, session_id):
        """Get full conversation history"""
        history = self.db.query(ConversationHistory).filter(
            ConversationHistory.session_id == session_id
        ).order_by(ConversationHistory.timestamp).all()
        
        return [h.to_dict() for h in history]
    
    def close(self):
        """Close database session"""
        self.db.close()
