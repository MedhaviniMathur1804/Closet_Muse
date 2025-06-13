# Fashion Recommender System

An open-source fashion recommendation system that suggests complementary clothing items based on uploaded images. The system uses computer vision and machine learning to analyze clothing items and provide personalized recommendations.

## Features

- Image upload support
- Clothing type classification
- Color analysis and matching
- Complementary item recommendations
- RESTful API endpoints
- React-based web interface
- MongoDB integration for product storage

## Tech Stack

### Frontend
- React.js with TypeScript
- TailwindCSS for styling
- Axios for API calls

### Backend
- FastAPI (Python)
- TensorFlow with MobileNetV2 for classification
- OpenCV for image processing
- FAISS for similarity search
- MongoDB for data storage
- Python libraries: NumPy, Pillow, scikit-learn

## Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB Community Edition
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fashion-recommender.git
cd fashion-recommender
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory:
```
MONGODB_URI=mongodb://localhost:27017/
```

## Running the Application

1. Start MongoDB:
```bash
mongod
```

2. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

3. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

- `GET /`: Health check
- `POST /upload`: Upload and analyze clothing image
- `GET /products`: Get all products
- `GET /products/{category}`: Get products by category
- `POST /products`: Add a new product
- `GET /products/{product_id}`: Get product by ID
- `PUT /products/{product_id}`: Update product
- `DELETE /products/{product_id}`: Delete product

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 