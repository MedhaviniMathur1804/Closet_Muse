from database.db import Database

def test_database_connection():
    try:
        # Initialize database
        db = Database()
        
        # Try to add a test product
        test_product = {
            'name': 'Test Product',
            'category': 'Test Category',
            'features': {'color': 'red', 'size': 'M'},
            'price': 99.99,
            'description': 'A test product',
            'image_url': 'http://example.com/test.jpg'
        }
        
        product_id = db.add_product(test_product)
        print(f"Successfully added test product with ID: {product_id}")
        
        # Try to retrieve the product
        retrieved_product = db.get_product(product_id)
        print(f"Successfully retrieved product: {retrieved_product}")
        
        # Clean up - delete the test product
        db.delete_product(product_id)
        print("Successfully deleted test product")
        
        print("All database operations completed successfully!")
        
    except Exception as e:
        print(f"Error testing database connection: {str(e)}")

if __name__ == "__main__":
    test_database_connection() 