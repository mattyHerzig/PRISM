#!/bin/sh -l

# Check for required environment variables
if [ -z "$LLAMA_API_KEY" ] || [ -z "$LLAMA_API_URL" ]; then
  echo "Error: Missing required environment variables LLAMA_API_KEY or LLAMA_API_URL"
  exit 1
fi

# Default filenames if not provided
DIFF_FILE="${1:-diff.txt}"
OUTPUT_FILE="${2:-output.txt}"
PR_FILE="${3:-pr.json}"

# Generate the PR description using main.py
echo "Generating PR description..."
python main.py --diff_file "$DIFF_FILE" --output_file "$OUTPUT_FILE" --pr_file "$PR_FILE"

# Display generated PR description for debugging purposes
echo "Generated PR description:"
cat "$OUTPUT_FILE"
