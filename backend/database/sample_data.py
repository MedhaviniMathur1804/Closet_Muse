from typing import List, Dict, Any

sample_products: List[Dict[str, Any]] = [
    {
        "name": "Classic White T-Shirt",
        "category": "top",
        "color": [255, 255, 255],
        "image": "https://example.com/white-tshirt.jpg",
        "features": {
            "style": "casual",
            "pattern": "solid",
            "season": ["spring", "summer"]
        }
    },
    {
        "name": "Blue Denim Jeans",
        "category": "bottom",
        "color": [0, 0, 139],
        "image": "https://example.com/blue-jeans.jpg",
        "features": {
            "style": "casual",
            "pattern": "solid",
            "season": ["all"]
        }
    },
    {
        "name": "Black Leather Jacket",
        "category": "outerwear",
        "color": [0, 0, 0],
        "image": "https://example.com/leather-jacket.jpg",
        "features": {
            "style": "edgy",
            "pattern": "solid",
            "season": ["fall", "winter"]
        }
    },
    {
        "name": "Floral Summer Dress",
        "category": "dress",
        "color": [255, 182, 193],
        "image": "https://example.com/floral-dress.jpg",
        "features": {
            "style": "feminine",
            "pattern": "floral",
            "season": ["spring", "summer"]
        }
    },
    {
        "name": "Brown Leather Boots",
        "category": "footwear",
        "color": [139, 69, 19],
        "image": "https://example.com/leather-boots.jpg",
        "features": {
            "style": "casual",
            "pattern": "solid",
            "season": ["fall", "winter"]
        }
    },
    {
        "name": "Silver Necklace",
        "category": "accessories",
        "color": [192, 192, 192],
        "image": "https://example.com/silver-necklace.jpg",
        "features": {
            "style": "elegant",
            "pattern": "solid",
            "season": ["all"]
        }
    }
]

def get_sample_products() -> List[Dict[str, Any]]:
    return sample_products 