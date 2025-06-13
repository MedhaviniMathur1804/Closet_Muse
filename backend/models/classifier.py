import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
from typing import Dict, Any

class ClothingClassifier:
    def __init__(self):
        # Load pre-trained MobileNetV2 model
        self.base_model = MobileNetV2(weights='imagenet', include_top=True)
        
        # Define clothing categories mapping
        self.categories = {
            'top': ['t-shirt', 'shirt', 'blouse', 'sweater', 'jacket'],
            'bottom': ['pants', 'jeans', 'skirt', 'shorts', 'suit', 'sarong'],
            'dress': ['dress'],
            'outerwear': ['coat', 'jacket'],
            'footwear': ['shoes', 'boots', 'sneakers']
        }

    def predict(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Predict the category of clothing in the image.
        Args:
            image: Preprocessed image array of shape (224, 224, 3)
        Returns:
            Dictionary containing prediction results
        """
        # Expand dimensions to create batch
        image_batch = np.expand_dims(image, axis=0)
        
        # Preprocess image for MobileNetV2
        preprocessed_image = preprocess_input(image_batch * 255.0)  # Scale back to 0-255 range
        
        # Get predictions
        predictions = self.base_model.predict(preprocessed_image)
        
        # Get top 5 predictions
        top_predictions = decode_predictions(predictions, top=5)[0]
        
        print("MobileNetV2 Top 5 Predictions:")
        for imagenet_id, label, confidence in top_predictions:
            print(f"- {label}: {confidence:.2f}")

        # Map predictions to clothing categories
        clothing_predictions = []
        for _, label, confidence in top_predictions:
            for category, items in self.categories.items():
                if any(item in label for item in items):
                    clothing_predictions.append({
                        'category': category,
                        'specific_item': label,
                        'confidence': float(confidence)
                    })
        
        # Sort by confidence
        clothing_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Return top prediction if any found, otherwise return None
        return {
            'predictions': clothing_predictions,
            'primary_category': clothing_predictions[0]['category'] if clothing_predictions else None
        } 