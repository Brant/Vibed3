#!/usr/bin/env python3
import os
import sys
import argparse
import json
from app.calendar_extractor import CalendarExtractor

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract events from calendar images')
    parser.add_argument('--images', '-i', nargs='+', help='Paths to calendar images')
    parser.add_argument('--output', '-o', default='calendar_events.json', help='Output JSON file path')
    parser.add_argument('--model', '-m', default='llama3', help='LLM model name')
    parser.add_argument('--all', '-a', action='store_true', help='Process all PNG files in current directory')

    args = parser.parse_args()

    # Initialize the calendar extractor
    extractor = CalendarExtractor(llm_model=args.model)

    # Determine which images to process
    image_paths = []
    if args.all:
        # Process all PNG files in the current directory
        for file in os.listdir('.'):
            if file.lower().endswith('.png'):
                image_paths.append(file)
    elif args.images:
        # Process specified images
        image_paths = args.images
    else:
        # Default to the three calendar images if no arguments provided
        image_paths = ['cal.png', 'cal2.png', 'cal3.png']

    # Check if any images were found
    if not image_paths:
        print("No images found to process.")
        sys.exit(1)

    print(f"Processing {len(image_paths)} images...")

    # Process images
    results = extractor.process_multiple_images(image_paths)

    # Save results to JSON
    success = extractor.save_results_to_json(results, args.output)

    if success:
        print(f"Results saved to {args.output}")

        # Print a summary of the results
        total_events = sum(len(events) for events in results.values())
        print(f"\nSummary: Found {total_events} events across {len(image_paths)} images")

        for image_path, events in results.items():
            print(f"\n{image_path}: {len(events)} events")

            # Print the first event as an example (if any)
            if events:
                print("Example event:")
                print(json.dumps(events[0], indent=2))
    else:
        print("Failed to save results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
