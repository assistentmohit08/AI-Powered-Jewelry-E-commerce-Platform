// src/components/ChatBot/ChatBot.jsx
import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import { chatbotAPI } from '../../services/api';
import { sessionStorage, scrollToBottom } from '../../utils/helpers';
import './ChatBot.css';

/**
 * ChatBot Component
 * 
 * Handles the main chatbot interface, including:
 * - Session management (creating/restoring sessions)
 * - Sending and receiving messages
 * - Displaying product recommendations
 * - Handling quick replies
 */
const ChatBot = ({ isOpen, onClose, onProductsReceived }) => {
  // --- State Management ---
  const [sessionId, setSessionId] = useState(null); // Stores the current chat session ID
  const [messages, setMessages] = useState([]); // Stores the history of chat messages
  const [inputValue, setInputValue] = useState(''); // Stores current input field value
  const [quickReplies, setQuickReplies] = useState([]); // Stores available quick reply options
  const [isTyping, setIsTyping] = useState(false); // Controls the typing indicator visibility

  // --- Refs ---
  const messagesEndRef = useRef(null); // Used to scroll to the bottom of the chat
  const messagesContainerRef = useRef(null); // Ref to the container for potential scroll calculations

  // --- Effects ---

  // Load session from sessionStorage on initial mount
  useEffect(() => {
    const savedSessionId = sessionStorage.load();
    if (savedSessionId) {
      setSessionId(savedSessionId);
    }
  }, []);

  // Initialize session when chat is opened if one doesn't exist
  useEffect(() => {
    if (isOpen && !sessionId) {
      startSession();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]); // Removed sessionId dependency to prevent double-firing

  // Scroll to bottom whenever messages change or typing status changes
  useEffect(() => {
    scrollToBottom(messagesContainerRef.current);
  }, [messages, isTyping]);

  /**
   * Starts a new chat session with the backend.
   */
  const startSession = async () => {
    setIsTyping(true);
    try {
      const data = await chatbotAPI.startSession();

      if (data.success) {
        const newSessionId = data.data.session_id;
        setSessionId(newSessionId);
        sessionStorage.save(newSessionId);

        // Add welcome message from server
        setMessages([{ text: data.data.message, isUser: false }]);

        // Set initial quick replies if any
        if (data.data.options && data.data.options.length > 0) {
          setQuickReplies(data.data.options);
        }
      }
    } catch (error) {
      console.error('Error starting session:', error);
      setMessages([
        {
          text: "Sorry, I'm having trouble connecting to the server. Please try again later.",
          isUser: false,
          isError: true // Flag to potentially style error messages differently
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  /**
   * Handles sending a message to the backend.
   * @param {string} [messageText] - Optional message text. If not provided, uses inputValue.
   */
  const sendMessage = async (messageText = null) => {
    const message = messageText || inputValue.trim();

    if (!message) return;

    // Optimistic UI updates
    setInputValue('');
    setQuickReplies([]); // Hide quick replies once a selection is made
    setMessages((prev) => [...prev, { text: message, isUser: true }]);
    setIsTyping(true);

    try {
      // Ensure we have a session ID before sending
      let currentSessionId = sessionId;
      if (!currentSessionId) {
        // Attempt to restore or restart if missing
        const saved = sessionStorage.load();
        if (saved) currentSessionId = saved;
        else {
          // Fallback: try to start a session first (simplified for this context)
          // Ideally we should await startSession() here but for now just using null
          // which might cause backend to generate a new one if handled.
        }
      }

      const data = await chatbotAPI.sendMessage(currentSessionId, message);

      if (data.success) {
        // Update session ID if backend returns a new/updated one
        if (data.data.session_id) {
          setSessionId(data.data.session_id);
          sessionStorage.save(data.data.session_id);
        }

        // Add bot response
        setMessages((prev) => [...prev, { text: data.data.message, isUser: false }]);

        // Update quick replies
        if (data.data.options && data.data.options.length > 0) {
          setQuickReplies(data.data.options);
        }

        // Handle product recommendations
        if (data.data.products && data.data.products.length > 0) {
          onProductsReceived(data.data.products);
        }
      } else {
        throw new Error(data.message || 'Unknown error from server');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          text: "Sorry, something went wrong. Please check your connection and try again.",
          isUser: false,
          isError: true
        },
      ]);
      // Only show retry if it was a user action? 
      // For simplicity, just showing error message is often enough in MVP.
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleQuickReply = (option) => {
    sendMessage(option);
  };

  if (!isOpen) return null;

  return (
    <div className={`chatbot-widget ${isOpen ? 'active' : ''}`}>
      {/* Header Section */}
      <div className="chatbot-header">
        <div className="chatbot-header-info">
          <div className="chatbot-avatar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"
                fill="currentColor"
              />
            </svg>
          </div>
          <div>
            <h3 className="chatbot-title">Jewelry Assistant</h3>
            <p className="chatbot-status">
              <span className="status-dot"></span>
              Online
            </p>
          </div>
        </div>
        <button className="chatbot-close" onClick={onClose} aria-label="Close Chat">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M18 6L6 18M6 6l12 12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>

      {/* Messages Area */}
      <div className="chatbot-messages" ref={messagesContainerRef}>
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
        ))}
        {/* Helper to ensure scrolling to bottom */}
        <div ref={messagesEndRef} />
      </div>

      {/* Typing Indicator */}
      {isTyping && (
        <div className="chatbot-typing">
          <div className="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="chatbot-input-area">
        <input
          type="text"
          className="chatbot-input"
          placeholder="Type your message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyPress} // Changed to onKeyDown for better modern browser support
          autoComplete="off"
        />
        <button className="chatbot-send" onClick={() => sendMessage()} aria-label="Send Message">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M18 2L9 11m9-9l-6 16-3-7-7-3 16-6z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>

      {/* Quick Replies Buttons */}
      {quickReplies.length > 0 && !isTyping && (
        <div className="quick-replies">
          {quickReplies.map((option, index) => (
            <button
              key={index}
              className="quick-reply-btn"
              onClick={() => handleQuickReply(option)}
            >
              {option}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatBot;