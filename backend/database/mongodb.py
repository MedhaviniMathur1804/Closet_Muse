from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

class MongoDB:
    def __init__(self):
        """Initialize MongoDB connection"""
        # Get MongoDB connection string from environment variable or use default
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.client: MongoClient = MongoClient(mongo_uri)
        self.db: Database = self.client.fashion_recommender
        self.products: Collection = self.db.products

    def get_all_products(self) -> List[Dict[str, Any]]:
        """Retrieve all products from the database"""
        return list(self.products.find())

    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieve products by category"""
        return list(self.products.find({"category": category}))

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single product by ID"""
        return self.products.find_one({"_id": product_id})

    def add_product(self, product_data: Dict[str, Any]) -> str:
        """Add a new product to the database"""
        # Add timestamps
        now = datetime.utcnow()
        product_data["created_at"] = now
        product_data["updated_at"] = now
        
        result = self.products.insert_one(product_data)
        return str(result.inserted_id)

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing product"""
        # Add updated timestamp
        updates["updated_at"] = datetime.utcnow()
        
        result = self.products.update_one(
            {"_id": product_id},
            {"$set": updates}
        )
        return result.modified_count > 0

    def delete_product(self, product_id: str) -> bool:
        """Delete a product from the database"""
        result = self.products.delete_one({"_id": product_id})
        return result.deleted_count > 0

    def close(self):
        """Close the MongoDB connection"""
        self.client.close() 