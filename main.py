#!/usr/bin/env python3
import os
import sys
import argparse
import json
from app.calendar_extractor import CalendarExtractor

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract events from a calendar image')
    parser.add_argument('image', nargs='?', help='Path to the calendar image to process')
    parser.add_argument('--output', '-o', help='Output JSON file path (defaults to [image_name]_events.json)')
    parser.add_argument('--model', '-m', default='llama3', help='LLM model name')

    args = parser.parse_args()

    # Handle the case when no image is provided
    if not args.image:
        print("Error: Please specify a calendar image to process.")
        print("Usage: python main.py path/to/calendar.png")
        sys.exit(1)

    # Check if the specified image exists
    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' does not exist.")
        sys.exit(1)

    # Set default output path if not provided
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.image))[0]
        args.output = f"{base_name}_events.json"

    print(f"Processing image: {args.image}")

    # Initialize the calendar extractor
    extractor = CalendarExtractor(llm_model=args.model)

    # Process the image
    events = extractor.process_image(args.image)

    # Save results to JSON
    try:
        with open(args.output, 'w') as f:
            json.dump(events, f, indent=2)
        print(f"Results saved to {args.output}")

        # Print a summary of the results
        print(f"\nSummary: Found {len(events)} events in {args.image}")

        # Print the first event as an example (if any)
        if events:
            print("\nExample event:")
            print(json.dumps(events[0], indent=2))
    except Exception as e:
        print(f"Error saving results to JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
