import os
import pytesseract
from PIL import Image
import numpy as np

class ImageProcessor:
    def __init__(self):
        """Initialize the image processor."""
        # Configure Tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'

    def extract_text_from_image(self, image_path):
        """
        Extract text from an image using OCR.

        Args:
            image_path (str): Path to the image file

        Returns:
            str: Extracted text from the image
        """
        try:
            # Open the image
            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Extract text using Tesseract OCR
            text = pytesseract.image_to_string(img)

            return text
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""

    def extract_text_with_positions(self, image_path):
        """
        Extract text with position data from an image.

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Dictionary containing text and position data
        """
        try:
            # Open the image
            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Extract text with position data
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            return data
        except Exception as e:
            print(f"Error extracting text with positions: {e}")
            return {}
