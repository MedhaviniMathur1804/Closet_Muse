from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProductBase(BaseModel):
    """Base model for product data"""
    name: str
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    price: float
    colors: List[str]
    style: Optional[str] = None
    description: Optional[str] = None
    image_url: str
    features: Dict[str, Any] = Field(default_factory=dict)

class ProductCreate(BaseModel):
    """Model for creating a new product, matching the script payload"""
    name: str
    category: str
    price: float
    description: str
    image_url: Optional[str] = None
    features: str

class ProductUpdate(BaseModel):
    """Model for updating an existing product"""
    name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    colors: Optional[List[str]] = None
    style: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[Dict[str, Any]] = None

class Product(ProductBase):
    """Complete product model including database fields"""
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 