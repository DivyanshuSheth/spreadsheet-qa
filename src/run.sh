#!/bin/bash

# Assign command-line arguments to variables
# IMAGE_DIR="./data/gold-imgs/sheet1-page1.png"
IMAGE_DIR="./data/gold-imgs/"
QUESTION="What is the sum of the pre-money valuation and post-money valuation?"
# QUESTION="What is the percentage of fully diluted shares for advisors?"
# QUESTION="What does this cap table assume about the options?"
# QUESTION="What are Series A preferred shares?"
# QUESTION="What is the number of outstanding shares?"
# QUESTION="What is the listed percentage ownership of common shares under share count by security type?"
# QUESTION="What does the textual description of Series A shares provided in the sheet say about where these shares are allocated?"
# QUESTION="What is the webpage link provided in the sheet?"
# QUESTION=""

# Call the Python script with the provided arguments and flags
python ./src/query_gpt.py --image_dir "$IMAGE_DIR" --question "$QUESTION"