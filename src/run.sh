#!/bin/bash

# Assign command-line arguments to variables
IMAGE_PATH="./data/gold-imgs/sheet1-page1.png"
QUESTION="What is the pre-money valuation for Series A?"

# Call the Python script with the provided arguments and flags
python ./src/query_gpt.py --image_path "$IMAGE_PATH" --question "$QUESTION"