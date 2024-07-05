import os
from pdf2image import convert_from_path
import zipfile

# Directory contains PDF
pdf_directory = './pdf/'

# Check if folder exist
if not os.path.exists(pdf_directory):
    print(f"This folder {pdf_directory} doesn't exist.")
else:
    # Search all files in the folder
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)

            # Create a folder for each PDF            
            pdf_name = os.path.splitext(filename)[0]
            output_directory = os.path.join(pdf_directory, pdf_name)
            os.makedirs(output_directory, exist_ok=True)

            try:
                # Convert PDF to images
                pages = convert_from_path(pdf_path)

                # Save each page into JPG image
                for i, page in enumerate(pages):
                    image_path = os.path.join(output_directory, f'page_{i+1:03}.jpg')
                    page.save(image_path, 'JPEG')
                    print(f"Page {i+1} of {pdf_name} save under {image_path}")

                # Create one ZIP file contained all JPG images only
                zip_path = os.path.join(pdf_directory, f'{pdf_name}.zip')
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for root, _, files in os.walk(output_directory):
                        for file in files:
                            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_directory))
                print(f"Folder {output_directory} zip under folder {zip_path}")

            except Exception as e:
                print(f"Error when try to convert {filename} : {e}")

# pdf-to-jpg-and-zip
# 