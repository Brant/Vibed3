import json
import os
import ollama

class LLMProcessor:
    def __init__(self, model_name="llama3"):
        """
        Initialize the LLM processor.

        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name

    def extract_events(self, ocr_text):
        """
        Extract event information from OCR text using LLM.

        Args:
            ocr_text (str): Text extracted from calendar image

        Returns:
            list: List of event dictionaries
        """
        prompt = f"""
        From the following calendar text, extract all events and organize them into structured data.
        For each event, provide:
        - Event title
        - Event description (if available)
        - Event date
        - Event time
        - Whether it is a repeating event, and what the repeating schedule is

        Calendar text:
        {ocr_text}

        Format your response as a valid JSON array of event objects. For example:
        [
            {{
                "title": "Team Meeting",
                "description": "Weekly status update",
                "date": "2023-04-15",
                "time": "10:00 AM - 11:00 AM",
                "repeating": true,
                "repeat_schedule": "Weekly on Tuesdays"
            }},
            {{
                "title": "Dentist Appointment",
                "description": "",
                "date": "2023-04-18",
                "time": "2:30 PM",
                "repeating": false,
                "repeat_schedule": ""
            }}
        ]

        Only respond with the JSON data, nothing else.
        """

        try:
            # Get response from Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the content from the response
            content = response['message']['content']

            # Find JSON in the response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Sometimes the model might return text around the JSON
                    # Try to clean it up
                    cleaned_json_str = self._clean_json_string(json_str)
                    return json.loads(cleaned_json_str)
            else:
                # Fallback if JSON parsing fails
                return self._parse_llm_output(content)

        except Exception as e:
            print(f"Error extracting events with LLM: {e}")
            return []

    def _clean_json_string(self, json_str):
        """
        Clean up JSON string that might have extra text or formatting issues.

        Args:
            json_str (str): JSON string to clean

        Returns:
            str: Cleaned JSON string
        """
        # This is a simple cleanup - could be extended for more complex cases
        lines = json_str.splitlines()
        cleaned_lines = []

        for line in lines:
            # Remove markdown code block syntax
            if line.strip().startswith('```') and (line.strip().endswith('```') or 'json' in line):
                continue
            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _parse_llm_output(self, text):
        """
        Fallback method to parse LLM output when JSON parsing fails.

        Args:
            text (str): Text output from LLM

        Returns:
            list: List of event dictionaries
        """
        # Simple parsing logic - this is a fallback
        events = []
        current_event = {}

        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "title" in line.lower() and ":" in line:
                # Start a new event if we find a title
                if current_event and "title" in current_event:
                    events.append(current_event)
                    current_event = {}

                parts = line.split(":", 1)
                if len(parts) == 2:
                    current_event["title"] = parts[1].strip()

            elif "description" in line.lower() and ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    current_event["description"] = parts[1].strip()

            elif "date" in line.lower() and ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    current_event["date"] = parts[1].strip()

            elif "time" in line.lower() and ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    current_event["time"] = parts[1].strip()

            elif "repeat" in line.lower() and ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    value = parts[1].strip().lower()
                    current_event["repeating"] = "yes" in value or "true" in value
                    if "schedule" in parts[0].lower():
                        current_event["repeat_schedule"] = parts[1].strip()

        # Add the last event if it exists
        if current_event and "title" in current_event:
            events.append(current_event)

        return events
