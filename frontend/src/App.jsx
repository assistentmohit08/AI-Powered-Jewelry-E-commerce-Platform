// src/App.jsx
import React, { useState } from 'react';
import Hero from './components/Hero/Hero';
import ProductsGrid from './components/Products/ProductsGrid';
import ChatBot from './components/ChatBot/ChatBot';
import ChatToggle from './components/ChatToggle/ChatToggle.jsx';
import './App.css';

/**
 * App Component
 * 
 * Main entry point for the application.
 * Manages global state such as:
 * - Chat window visibility
 * - Product data received from the chatbot
 * - Global notifications
 */
function App() {
  // --- State Configuration ---
  const [isChatOpen, setIsChatOpen] = useState(false); // Controls chat window visibility
  const [products, setProducts] = useState([]); // Stores list of products to display
  const [showProducts, setShowProducts] = useState(false); // Controls if the product grid is visible
  const [hasNotification, setHasNotification] = useState(false); // Notification badge state for chat

  // --- Handlers ---

  /**
   * Opens the chat window and clears notifications.
   */
  const handleOpenChat = () => {
    setIsChatOpen(true);
    setHasNotification(false);
  };

  /**
   * Closes the chat window.
   */
  const handleCloseChat = () => {
    setIsChatOpen(false);
  };

  /**
   * Toggles the chat window open/closed.
   */
  const handleToggleChat = () => {
    if (isChatOpen) {
      handleCloseChat();
    } else {
      handleOpenChat();
    }
  };

  /**
   * Handler for when products are received from the ChatBot backend.
   * Updates product list, shows the grid, and manages focus/scroll interactions.
   * @param {Array} newProducts - Array of product objects.
   */
  const handleProductsReceived = (newProducts) => {
    setProducts(newProducts);
    setShowProducts(true);

    // Scroll to recommendations section after a short delay to ensure DOM update
    setTimeout(() => {
      const section = document.getElementById('recommendationsSection');
      if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 500);

    // Automatically close chatbot to reveal products (UX choice)
    setTimeout(() => {
      handleCloseChat();
    }, 2000);
  };

  return (
    <div className="App">
      {/* Hero Section: Welcome screen and initial Call to Action */}
      <Hero onStartChat={handleOpenChat} />

      {/* Products Grid: Displays recommendations when available */}
      <ProductsGrid
        products={products}
        visible={showProducts}
      />

      {/* ChatBot Widget: The main interaction component */}
      <ChatBot
        isOpen={isChatOpen}
        onClose={handleCloseChat}
        onProductsReceived={handleProductsReceived}
      />

      {/* Chat Toggle Button: Floating button to reopen chat */}
      <ChatToggle
        isOpen={isChatOpen}
        onClick={handleToggleChat}
        hasNotification={hasNotification}
      />
    </div>
  );
}

export default App;