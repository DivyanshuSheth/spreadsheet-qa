import argparse
import os
import pandas as pd
import jpype
import asposecells
jpype.startJVM()
from pdf2image import convert_from_path
from asposecells.api import Workbook, SaveFormat

def main(input_excel, output_dir):
    # Check if output directory exists, if not, create it
    print(f"Input Excel: {input_excel}")
    print(f"Output Directory: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # File paths
    pdf_path = os.path.join(output_dir, "sheet.pdf")

    # Step 1: Read Excel file into a Pandas DataFrame (optional, can be removed if not needed)
    df = pd.read_excel(input_excel, sheet_name=0)

    # Step 2: Convert Pandas DataFrame to PDF using Aspose.Cells
    workbook = Workbook(input_excel)
    workbook.save(pdf_path, SaveFormat.PDF)

    # Step 3: Convert PDF to images using pdf2image
    images = convert_from_path(pdf_path)

    # Save each page as an image file
    for i, image in enumerate(images):
        image.save(os.path.join(output_dir, f'page_{i}.png'))

    print(f"Conversion complete. Images are saved in {output_dir}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Convert Excel to PDF and PDF to PNG images")
    parser.add_argument('--input_excel', type=str, help="Path to the input Excel (.xlsx) file")
    parser.add_argument('--output_dir', type=str, help="Path to the output directory where PNG files will be saved")

    args = parser.parse_args()
    main(args.input_excel, args.output_dir)