# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 21:14:49 2024

@author: roope
"""

import requests
import json
from pymongo import MongoClient
from PIL import Image

# The URL you want to send the POST request to
url = 'https://mlaas.precise-lab.com/supplement'

# The path to the image file you want to send
image_file_path = 'C:/Users/roope/Documents/Capstone Project- Product Label Recognition/mtndew2.jpg'   # Replace with the actual path to your image file

# Open and save the image using Pillow to ensure it's in the correct format
image = Image.open(image_file_path)
image.save('C:/Users/roope/Documents/Capstone Project- Product Label Recognition/converted_mtndew2.jpg' )  # Save the image in JPEG format

# Convert the image to PDF
pdf_file_path = 'C:/Users/roope/Documents/Capstone Project- Product Label Recognition/convertedmtndew2.pdf'   # Path where the PDF file will be saved
pdf = FPDF()
pdf.add_page()
pdf.image('C:/Users/roope/Documents/Capstone Project- Product Label Recognition/converted_mtndew2.jpg' , x=10, y=10, w=190)
pdf.output(pdf_file_path, "F")

# Open the PDF file in binary mode
with open(pdf_file_path, 'rb') as pdf_file:
    # Define the files parameter as a dictionary
    # The key is the name of the form field for file upload (e.g., 'file')
    # The value is a tuple consisting of:
    # - The filename (or you can set it as None)
    # - The file object
    files = {'file': (pdf_file_path.split('/')[-1], pdf_file)}

    # Send the POST request with the PDF file
    response = requests.post(url, files=files, verify=False)

# Check if the request was successful
if response.status_code == 200:
    print("File uploaded successfully")
    # Process the response
    json_data = response.json()
    print(json_data)
    
    # Store JSON data in MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Precise']  # Replace 'your_database' with the name of your MongoDB database
    collection = db['ProductLabels']  # Replace 'your_collection' with the name of your MongoDB collection
    collection.insert_one(json_data)
    print("JSON data stored in MongoDB")
else:
    print("Failed to upload the file")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
