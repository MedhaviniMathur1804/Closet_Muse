import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Tuple, List

class ImageProcessor:
    @staticmethod
    def extract_dominant_colors(image: np.ndarray, n_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from an image using K-means clustering."""
        # Reshape the image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Convert to float32
        pixels = np.float32(pixels)
        
        # Define criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        
        # Apply k-means clustering
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        
        # Convert back to uint8
        palette = np.uint8(palette)
        
        # Get the counts of each color
        unique_labels, counts = np.unique(labels, return_counts=True)
        
        # Sort colors by frequency
        sorted_indices = np.argsort(-counts)
        sorted_colors = palette[sorted_indices]
        
        # Convert to RGB tuples
        return [tuple(color) for color in sorted_colors.tolist()]

    @staticmethod
    def preprocess_image(image_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """Preprocess image for model input."""
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values
        image_array = image_array.astype(np.float32) / 255.0
        
        return image_array

    @staticmethod
    def get_image_features(image: np.ndarray) -> dict:
        """Extract various features from the image."""
        # Get dominant colors
        dominant_colors = ImageProcessor.extract_dominant_colors(image)
        
        # Calculate average brightness
        brightness = np.mean(image)
        
        # Calculate color histogram
        hist = cv2.calcHist([image], [0, 1, 2], None, [16, 16, 16], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        return {
            'dominant_colors': dominant_colors,
            'brightness': float(brightness),
            'color_histogram': hist.tolist()
        } 