// src/components/Products/ProductCard.jsx
import React, { useEffect } from 'react';
import { formatPrice } from '../../utils/helpers';
import { chatbotAPI } from '../../services/api';

const ProductCard = ({ product, sessionId, index }) => {
  useEffect(() => {
    // Track view when card is mounted
    if (sessionId && product.id) {
      chatbotAPI.trackInteraction(sessionId, product.id, 'view');
    }
  }, [sessionId, product.id]);

  const handleClick = () => {
    if (sessionId && product.id) {
      chatbotAPI.trackInteraction(sessionId, product.id, 'click');
    }
    // Could open product details modal here
    console.log('Product clicked:', product);
  };

  const handleImageError = (e) => {
    e.target.src = 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400';
  };

  return (
    <div
      className="product-card"
      style={{ animationDelay: `${index * 0.1}s` }}
      onClick={handleClick}
    >
      <img
        src={product.image_url}
        alt={product.name}
        className="product-image"
        onError={handleImageError}
      />
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <div className="product-meta">
          {product.category && (
            <span className="product-tag">{product.category}</span>
          )}
          {product.metal_type && (
            <span className="product-tag">{product.metal_type}</span>
          )}
          {product.style && <span className="product-tag">{product.style}</span>}
        </div>
        <div className="product-price">{formatPrice(product.price)}</div>
        {product.description && (
          <p className="product-description">{product.description}</p>
        )}
      </div>
    </div>
  );
};

export default ProductCard;