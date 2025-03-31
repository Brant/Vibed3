import os
import json
from app.image_processor import ImageProcessor
from app.llm_processor import LLMProcessor

class CalendarExtractor:
    def __init__(self, llm_model="llama3"):
        """
        Initialize the calendar extractor.

        Args:
            llm_model (str): Name of the LLM model to use
        """
        self.image_processor = ImageProcessor()
        self.llm_processor = LLMProcessor(model_name=llm_model)

    def process_image(self, image_path):
        """
        Process a calendar image and extract events.

        Args:
            image_path (str): Path to the calendar image

        Returns:
            list: List of extracted events
        """
        # Extract text from the image
        ocr_text = self.image_processor.extract_text_from_image(image_path)

        # Use LLM to extract events from the OCR text
        events = self.llm_processor.extract_events(ocr_text)

        return events

    def process_multiple_images(self, image_paths):
        """
        Process multiple calendar images and extract events.

        Args:
            image_paths (list): List of paths to calendar images

        Returns:
            dict: Dictionary with image paths as keys and lists of events as values
        """
        results = {}

        for image_path in image_paths:
            events = self.process_image(image_path)
            results[image_path] = events

        return results

    def save_results_to_json(self, results, output_path):
        """
        Save extraction results to a JSON file.

        Args:
            results (dict): Dictionary with image paths as keys and lists of events as values
            output_path (str): Path to save the JSON file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving results to JSON: {e}")
            return False
