// src/components/ChatToggle/ChatToggle.jsx
import React from 'react';
import './ChatToggle.css';

const ChatToggle = ({ isOpen, onClick, hasNotification }) => {
  return (
    <button className={`chatbot-toggle ${isOpen ? 'active' : ''}`} onClick={onClick}>
      <svg
        className="chat-icon"
        width="28"
        height="28"
        viewBox="0 0 28 28"
        fill="none"
        style={{ display: isOpen ? 'none' : 'block' }}
      >
        <path
          d="M14 2C7.373 2 2 6.82 2 12.8c0 3.445 1.832 6.505 4.667 8.4v4.8l4.4-2.4c1.267.267 2.6.4 3.933.4 6.627 0 12-4.82 12-10.8S20.627 2 14 2z"
          fill="currentColor"
        />
      </svg>
      <svg
        className="close-icon"
        width="28"
        height="28"
        viewBox="0 0 28 28"
        fill="none"
        style={{ display: isOpen ? 'block' : 'none' }}
      >
        <path
          d="M21 7L7 21M7 7l14 14"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </svg>
      {hasNotification && !isOpen && (
        <span className="notification-badge">1</span>
      )}
    </button>
  );
};

export default ChatToggle;