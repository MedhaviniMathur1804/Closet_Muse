import numpy as np
from typing import List, Dict, Any
import faiss
from sklearn.preprocessing import normalize
import json # Import json

class FashionRecommender:
    def __init__(self):
        # Initialize empty product database
        self.products: List[Dict[str, Any]] = []
        self.feature_vectors: np.ndarray = None
        self.index = None
        
        # Define complementary categories
        self.complementary_categories = {
            'top': ['bottom', 'accessories'],
            'bottom': ['top', 'footwear', 'accessories'],
            'dress': ['footwear', 'accessories'],
            'outerwear': ['top', 'bottom', 'accessories'],
            'footwear': ['bottom', 'accessories']
        }
        
        # Color compatibility rules
        self.color_compatibility = {
            'monochromatic': lambda c1, c2: self._is_monochromatic(c1, c2),
            'complementary': lambda c1, c2: self._is_complementary(c1, c2),
            'analogous': lambda c1, c2: self._is_analogous(c1, c2)
        }

    def add_product(self, product: Dict[str, Any], features: np.ndarray):
        """Add a product and its features to the database."""
        print(f"Adding product to recommender: {product.get('name')}") # Added print statement
        self.products.append(product)
        
        if self.feature_vectors is None:
            self.feature_vectors = features.reshape(1, -1)
        else:
            self.feature_vectors = np.vstack([self.feature_vectors, features.reshape(1, -1)])
        
        # Rebuild the index
        self._build_index()

    def _build_index(self):
        """Build FAISS index for fast similarity search."""
        if len(self.products) == 0:
            print("No products to build index.") # Added print statement
            return
        
        print(f"Building FAISS index with {len(self.products)} vectors.") # Added print statement
        # Normalize feature vectors
        normalized_features = normalize(self.feature_vectors)
        
        # Build index
        dimension = self.feature_vectors.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(normalized_features.astype('float32'))

    def get_recommendations(self, query_features, category=None, top_k=5):
        # Recommend from the same category as the query
        filtered_products = [p for p in self.products if p['category'] == category]
        print("All product categories:", [p['category'] for p in self.products])
        print("Target category:", category)
        # If no products in the same category, return empty list
        if not filtered_products:
            return []
        # Prepare feature vectors for filtered products
        filtered_features = np.array([
            self.feature_vectors[idx]
            for idx, p in enumerate(self.products)
            if p['category'] == category
        ])
        # Normalize query and product features
        normalized_query = query_features.reshape(1, -1)
        normalized_query = normalized_query / np.linalg.norm(normalized_query)
        normalized_features = filtered_features / np.linalg.norm(filtered_features, axis=1, keepdims=True)
        # Compute distances
        dists = np.linalg.norm(normalized_features - normalized_query, axis=1)
        # Get top_k indices
        top_indices = np.argsort(dists)[:top_k]
        # Return the top_k recommended products
        return [filtered_products[i] for i in top_indices]

    def _is_monochromatic(self, color1: List[int], color2: List[int]) -> bool:
        """Check if two colors are monochromatic (same hue, different brightness)."""
        threshold = 50
        return sum(abs(c1 - c2) for c1, c2 in zip(color1, color2)) < threshold

    def _is_complementary(self, color1: List[int], color2: List[int]) -> bool:
        """Check if two colors are complementary (opposite on color wheel)."""
        # Simple implementation - can be improved with proper color wheel calculations
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return abs(r1 - r2) > 127 and abs(g1 - g2) > 127 and abs(b1 - b2) > 127

    def _is_analogous(self, color1: List[int], color2: List[int]) -> bool:
        """Check if two colors are analogous (adjacent on color wheel)."""
        # Simple implementation - can be improved with proper color wheel calculations
        threshold = 50
        return sum(abs(c1 - c2) for c1, c2 in zip(color1, color2)) < threshold * 3 