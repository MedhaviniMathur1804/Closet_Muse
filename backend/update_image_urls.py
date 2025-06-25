import requests
import os

BACKEND_URL = "http://localhost:8000"

def update_image_urls():
    # Get all products
    response = requests.get(f"{BACKEND_URL}/products")
    products = response.json()

    for product in products:
        product_id = product['id']
        old_url = product.get('image_url', '')
        if old_url:
            filename = os.path.basename(old_url)
            new_url = f"http://localhost:8000/static/{filename}"
            if old_url != new_url:
                # Prepare the update payload
                update_payload = {"image_url": new_url}
                # Send the update request
                put_response = requests.put(f"{BACKEND_URL}/products/{product_id}", json=update_payload)
                if put_response.status_code == 200:
                    print(f"Updated product {product_id}: {old_url} -> {new_url}")
                else:
                    print(f"Failed to update product {product_id}: {put_response.text}")

if __name__ == "__main__":
    update_image_urls() 