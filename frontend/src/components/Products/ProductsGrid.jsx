// src/components/Products/ProductsGrid.jsx
import React from 'react';
import ProductCard from './ProductCard';
import './Products.css';

const ProductsGrid = ({ products, sessionId, visible }) => {
  if (!visible) return null;

  return (
    <section className="recommendations-section" id="recommendationsSection">
      <div className="container">
        <h2 className="section-title">Your Personalized Recommendations</h2>
        <div className="products-grid">
          {products && products.length > 0 ? (
            products.map((product, index) => (
              <ProductCard
                key={product.id}
                product={product}
                sessionId={sessionId}
                index={index}
              />
            ))
          ) : (
            <div className="no-products-message">
              <p>No products found matching your current filters. Try adjusting your preferences! 💎</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProductsGrid;