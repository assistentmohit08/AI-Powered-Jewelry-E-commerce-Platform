// src/components/Hero/Hero.jsx
import React from 'react';
import './Hero.css';

const Hero = ({ onStartChat }) => {
  return (
    <header className="hero">
      <div className="hero-content">
        <h1 className="hero-title">
          <span className="gradient-text">Discover Your Perfect</span>
          <br />
          Jewelry Match
        </h1>
        <p className="hero-subtitle">Let our AI assistant guide you to the perfect piece</p>
        <button className="cta-button" onClick={onStartChat}>
          <span>Start Your Journey</span>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M4 10h12m-6-6l6 6-6 6"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
      <div className="hero-decoration">
        <div className="floating-gem gem-1"></div>
        <div className="floating-gem gem-2"></div>
        <div className="floating-gem gem-3"></div>
      </div>
    </header>
  );
};

export default Hero;