print("Attempting to run clear_db.py")
from database.db import Database

def clear_database():
    db = Database()
    print("Attempting to delete all products...")
    try:
        deleted_count = db.delete_all_products()
        print(f"Successfully deleted {deleted_count} products.")
    except Exception as e:
        print(f"Failed to delete products: {e}")

if __name__ == "__main__":
    clear_database() 