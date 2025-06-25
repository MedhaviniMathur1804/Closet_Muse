import requests
import json
import numpy as np
import os
import sys
from dotenv import load_dotenv
from typing import Dict, Any

# Import backend components for feature extraction and classification
# Ensure your virtual environment is active and these modules are accessible
from utils.image_processor import ImageProcessor
from models.classifier import ClothingClassifier

# Load environment variables (including DATABASE_URL if used)
load_dotenv()

# Assuming your backend is running on localhost:8000
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

# Initialize image processor and classifier
image_processor = ImageProcessor()
classifier = ClothingClassifier()

def add_product_from_image(image_path: str, name: str, price: float, description: str, image_url: str = None, force_category: str = None):
    try:
        # Read image file content
        with open(image_path, 'rb') as f:
            image_content = f.read()

        # Preprocess image
        processed_image = image_processor.preprocess_image(image_content)

        # Extract image features
        image_features = image_processor.get_image_features(processed_image)

        # Classify the clothing
        if force_category:
            category = force_category
        else:
            classification_result = classifier.predict(processed_image)
            if not classification_result['primary_category']:
                print(f"Error: Could not classify the clothing item in {image_path}")
                return
            category = classification_result['primary_category']

        # Prepare product data
        product_data = {
            "name": name,
            "category": category,
            "price": price,
            "description": description,
            "image_url": image_url if image_url else os.path.abspath(image_path),
            "features": json.dumps({
                "color_histogram": image_features['color_histogram'],
                "dominant_colors": image_features['dominant_colors'],
                "brightness": image_features['brightness']
            })
        }

        # Add product to database via backend API
        endpoint_url = f"{BACKEND_URL}/products"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(endpoint_url, headers=headers, json=product_data)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        print(f"Successfully added product from {image_path}:", response.json())

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding product via API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python add_product_from_image.py <image_path> <name> <price> <description> [image_url]")
        sys.exit(1)

    image_path = sys.argv[1]
    name = sys.argv[2]
    price = float(sys.argv[3])
    description = sys.argv[4]
    image_url = sys.argv[5] if len(sys.argv) > 5 else None

    filename = os.path.basename(image_path)
    if filename.startswith("accessory"):
        force_category = "accessories"
    elif filename.startswith("footwear"):
        force_category = "footwear"
    elif filename.startswith("top"):
        force_category = "top"
    elif filename.startswith("bottom"):
        force_category = "bottom"
    else:
        force_category = None

    add_product_from_image(image_path, name, price, description, image_url, force_category) 