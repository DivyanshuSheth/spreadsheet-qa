#!/bin/bash

EXCEL_PATH="/home/dasheth/ema/spreadsheet-qa/data/xlsx/Capitalization Table - Series A Example.xlsx"
IMAGE_DIR="/home/dasheth/ema/spreadsheet-qa/data/pngs"

QUESTION="What is the sum of the Series A and Series B funding? Get both amounts separately individually and sum them."
# QUESTION="What is the outstanding Series A liquidation preference amount?"
# QUESTION="What is the sum of the pre-money valuation and post-money valuation?"
# QUESTION="What is the percentage of fully diluted shares for advisors?"
# QUESTION="What does this cap table assume about the options?"
# QUESTION="What are Series A preferred shares?"
# QUESTION="What is the number of outstanding shares?"
# QUESTION="What is the listed percentage ownership of common shares under share count by security type?"
# QUESTION="What does the textual description of Series A shares provided in the sheet say about where these shares are allocated?"
# QUESTION="What is the webpage link provided in the sheet?"

python ./src/convert_excel_to_images.py --input_excel "$EXCEL_PATH" --output_dir "$IMAGE_DIR"

# Call the Python script with the provided arguments and flags
python ./src/query_gpt4o.py --image_dir "$IMAGE_DIR" --question "$QUESTION"