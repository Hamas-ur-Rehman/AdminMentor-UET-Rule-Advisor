from pdf2image import convert_from_path
import easyocr
from tqdm import tqdm
import os
import concurrent.futures
import numpy as np
import poppler
import time
import shutil
poppler.poppler_path='C:\\poppler-24.07.0\\bin\\'


def process_page(img, i, output_folder, reader):
    # Convert PIL Image to NumPy array
    img_np = np.array(img)
    # Convert image to text using EasyOCR
    text = reader.readtext(img_np, detail=0, paragraph=True)
    text = '\n'.join(text)
    if text.strip():
        output_file_path = os.path.join(output_folder, f'page_{i + 1}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

def extract_text_from_pdf(pdf_path, limit=None):
    reader = easyocr.Reader(['en'], gpu=True)  # Use GPU for OCR

    # Convert PDF to images
    timer = time.time()
    images = convert_from_path(pdf_path)
    print(f"Time taken to convert PDF to images: {(time.time()-timer):.2f} seconds")
    
    if limit:
        images = images[0:limit]
    
    output_folder = 'extracted'
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)


    # Extract text from images in parallel
    timer = time.time()
    with tqdm(total=len(images), desc="Extracting text", unit="page") as pbar:
        for i, img in enumerate(images):
            process_page(img, i, output_folder, reader)
            pbar.update(1)
    print(f"Time taken to extract text from images: {(time.time()-timer):.2f} seconds")
    

    print(f"Text extracted and saved to '{output_folder}' folder.")

# Example usage:
pdf_path = 'dataset/dataset.pdf'
extract_text_from_pdf(pdf_path, limit=262)
