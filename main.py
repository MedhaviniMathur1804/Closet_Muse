print("Backend application starting...")
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from typing import List, Dict, Any
import json
from fastapi.staticfiles import StaticFiles

from utils import image_processor
from models.product import ProductCreate
from utils.image_processor import ImageProcessor
from models.classifier import ClothingClassifier
from models.recommender import FashionRecommender
from database.db import Database

app = FastAPI()

# Allow frontend on port 3000 (React default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
image_processor = ImageProcessor()
classifier = ClothingClassifier()
recommender = FashionRecommender()
db = Database()

# Load products from database into recommender on startup
products_from_db = db.get_all_products()
for p in products_from_db:
    print(f"Processing product ID: {p.get('id')}")
    print(f"Product data from DB: {p}")
    # Ensure features are a numpy array if available
    features = None
    if 'features' in p and isinstance(p['features'], dict):
        try:
            # features_dict is already a dict from db.get_all_products
            features_dict = p['features']
            # Removed the json.loads call as it's already done in db.py
            # print(f"Product ID {p.get('id')}: Raw features string = {p['features']}") # Removed this print
            print(f"Product ID {p.get('id')}: Parsed features dict = {features_dict}") # Kept this print
            if 'color_histogram' in features_dict:
                print(f"Product ID {p.get('id')}: Color histogram before np.array = {features_dict['color_histogram']}") # Kept this print
                features = np.array(features_dict['color_histogram'])
            else:
                print(f"Warning: 'color_histogram' not found in features for product ID {p.get('id')}")
        except Exception as e:
            print(f"Warning: Error processing features for product ID {p.get('id')}: {e}")
            continue # Skip product if features processing fails
    
    print(f"Product ID {p.get('id')}: Processed features = {features}")

    if features is not None:
        category = p.get('category')  # e.g., "top", "bottom", "footwear", "accessories"
        image_filename = f"{category}_{p.get('id')}.png"
        image_url = f"http://localhost:8000/static/{image_filename}"
        p['image_url'] = image_url
        recommender.add_product(p, features)

print(f"Loaded {len(recommender.products)} products into the recommender on startup.")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Fashion Recommender API is working!"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        # Read image file
        contents = await file.read()
        
        # Preprocess image
        processed_image = image_processor.preprocess_image(contents)
        
        # Extract image features
        image_features = image_processor.get_image_features(processed_image)
        
        # Classify the clothing
        classification_result = classifier.predict(processed_image)
        
        if not classification_result['primary_category']:
            raise HTTPException(status_code=400, detail="Could not classify the clothing item")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            query_features=np.array(image_features['color_histogram']),
            category=classification_result['primary_category']
        )
        
        return {
            "classification": classification_result,
            "features": image_features,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
def get_products(category: str = None) -> List[Dict[str, Any]]:
    try:
        if category:
            return db.get_products_by_category(category)
        return db.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products")
def create_product(product: ProductCreate) -> Dict[str, int]:
    try:
        # Convert Pydantic model to dictionary for db.add_product
        product_data = product.model_dump()
        
        # db.add_product expects features as a JSON string, which ProductCreate already provides
        product_id = db.add_product(product_data)
        return {"id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}")
def get_product(product_id: str) -> Dict[str, Any]:
    try:
        # db.get_product expects product_id as int, need to convert
        product = db.get_product(int(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/products/{product_id}")
def update_product(product_id: str, updates: Dict[str, Any]) -> Dict[str, bool]:
    try:
        # db.update_product expects product_id as int, need to convert
        success = db.update_product(int(product_id), updates)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/products/{product_id}")
def delete_product(product_id: str) -> Dict[str, bool]:
    try:
        # db.delete_product expects product_id as int, need to convert
        success = db.delete_product(int(product_id))
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

