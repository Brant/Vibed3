# Calendar Event Extractor

A system that extracts event information from calendar images using OCR and an open-source LLM.

## Features

- Extracts event details from calendar images:
  - Event title
  - Event description (if available)
  - Event date
  - Event time
  - Repetition information
- Uses Tesseract OCR for text extraction
- Uses Ollama with open-source LLM models for event extraction
- Outputs structured JSON data

## Prerequisites

- Python 3.8+
- Tesseract OCR (must be installed separately)
- Ollama (must be installed separately)

## Installation

1. Install Tesseract OCR:
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`
   - Windows: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

2. Install Ollama:
   - Follow instructions at [Ollama website](https://ollama.ai/download)

3. Pull the Llama 3 model:
   ```
   ollama pull llama3
   ```

4. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```
python main.py cal.png
```

This will process the specified calendar image (`cal.png`) and save the results to `cal_events.json`.

### Advanced Usage

```
python main.py cal.png --output results.json --model llama3
```

Options:
- `--output`, `-o`: Output JSON file path (default: [image_name]_events.json)
- `--model`, `-m`: LLM model name to use with Ollama (default: llama3)

## Output Format

The output JSON file contains an array of event objects:

```json
[
  {
    "title": "Team Meeting",
    "description": "Weekly status update",
    "date": "2023-04-15",
    "time": "10:00 AM - 11:00 AM",
    "repeating": true,
    "repeat_schedule": "Weekly on Tuesdays"
  },
  {
    "title": "Dentist Appointment",
    "description": "",
    "date": "2023-04-18",
    "time": "2:30 PM",
    "repeating": false,
    "repeat_schedule": ""
  }
]
```

## Limitations

- The accuracy depends on the quality of the calendar image and the OCR process
- The LLM may not always correctly identify all event details
- Processing large or complex calendar images may require adjustments to the OCR settings

## License

MIT 
