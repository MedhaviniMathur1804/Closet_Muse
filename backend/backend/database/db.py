from sqlalchemy import create_engine, Column, String, Integer, Float, JSON, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
import json

load_dotenv()

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    features = Column(Text)  # Store JSON as text
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)

    __table_args__ = (
        Index('idx_category', 'category'),
    )

class Database:
    def __init__(self):
        # Get PostgreSQL connection string from environment variable or use default
        db_url = os.getenv('DATABASE_URL', 'postgresql://fashion_user:fashion_password@localhost:5432/fashion_recommender')
        self.engine = create_engine(db_url)
        # Check if tables exist, if not, create them. This is done automatically by create_all
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_product(self, product: Dict[str, Any]) -> int:
        """Add a product to the database."""
        session = self.Session()
        try:
            # Convert features dict to JSON string
            if 'features' in product and isinstance(product['features'], dict):
                # This conversion is now handled before calling this method by the script/endpoint
                # But we keep the check just in case.
                import json
                product['features'] = json.dumps(product['features'])

            # Ensure product dictionary only contains keys that map to Product model columns
            # Filter out any extra keys if necessary, though Pydantic model should handle this for POST
            valid_keys = [c.name for c in Product.__table__.columns]
            product_data_filtered = {k: v for k, v in product.items() if k in valid_keys}

            db_product = Product(**product_data_filtered)
            session.add(db_product)
            session.commit()
            # Refresh the instance to get the generated ID
            session.refresh(db_product)
            return db_product.id
        except Exception as e:
            session.rollback() # Rollback in case of error
            raise e # Re-raise the exception
        finally:
            session.close()

    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get a product by ID."""
        session = self.Session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                # Convert SQLAlchemy model instance to dictionary
                result = {
                    'id': product.id,
                    'name': product.name,
                    'category': product.category,
                    'price': product.price,
                    'description': product.description,
                    'image_url': product.image_url,
                    'features': json.loads(product.features) if product.features else None # Parse JSON string back to dict
                }
                return result
            return None
        finally:
            session.close()

    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all products in a category."""
        session = self.Session()
        try:
            products = session.query(Product).filter(Product.category == category).all()
            result = []
            for p in products:
                 product_dict = {
                    'id': p.id,
                    'name': p.name,
                    'category': p.category,
                    'price': p.price,
                    'description': p.description,
                    'image_url': p.image_url,
                    'features': json.loads(p.features) if p.features else None # Parse JSON string back to dict
                }
                 result.append(product_dict)
            return result
        finally:
            session.close()

    def update_product(self, product_id: int, updates: Dict[str, Any]) -> bool:
        """Update a product."""
        session = self.Session()
        try:
            # Convert features dict to JSON string if present
            if 'features' in updates and isinstance(updates['features'], dict):
                 import json
                 updates['features'] = json.dumps(updates['features'])
            
            result = session.query(Product).filter(Product.id == product_id).update(updates)
            session.commit()
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_product(self, product_id: int) -> bool:
        """Delete a product."""
        session = self.Session()
        try:
            result = session.query(Product).filter(Product.id == product_id).delete()
            session.commit()
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_all_products(self) -> int:
        """Delete all products from the database."""
        session = self.Session()
        try:
            # Delete all rows from the Product table
            num_deleted = session.query(Product).delete()
            session.commit()
            print(f"Deleted {num_deleted} products from the database.")
            return num_deleted
        except Exception as e:
            session.rollback()
            print(f"Error deleting all products: {e}")
            raise e
        finally:
            session.close()

    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products."""
        session = self.Session()
        try:
            products = session.query(Product).all()
            print(f"Database found {len(products)} products.") # Added print statement
            result = []
            for p in products:
                product_dict = {
                    'id': p.id,
                    'name': p.name,
                    'category': p.category,
                    'price': p.price,
                    'description': p.description,
                    'image_url': p.image_url,
                    'features': json.loads(p.features) if p.features else None # Parse JSON string back to dict
                }
                result.append(product_dict)
            return result
        except Exception as e:
            print(f"Error fetching all products from database: {e}") # Added error print
            raise e
        finally:
            session.close() 