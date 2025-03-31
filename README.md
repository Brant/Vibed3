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
python main.py
```

This will process the default images (`cal.png`, `cal2.png`, `cal3.png`) and save the results to `calendar_events.json`.

### Advanced Usage

```
python main.py --images image1.png image2.png --output results.json --model llama3
```

Options:
- `--images`, `-i`: Paths to calendar images to process
- `--output`, `-o`: Output JSON file path (default: calendar_events.json)
- `--model`, `-m`: LLM model name to use with Ollama (default: llama3)
- `--all`, `-a`: Process all PNG files in the current directory

## Output Format

The output JSON file contains a dictionary with image paths as keys and lists of event objects as values:

```json
{
  "cal.png": [
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
  ],
  "cal2.png": [
    // Events from cal2.png
  ]
}
```

## Limitations

- The accuracy depends on the quality of the calendar image and the OCR process
- The LLM may not always correctly identify all event details
- Processing large or complex calendar images may require adjustments to the OCR settings

## License

MIT 
