import requests

# The URL you want to send the POST request to
url = 'https://mlaas.precise-lab.com/supplement'

# The path to the PDF file you want to send
file_path_milk_dried_prods_09 = '/Users/saisharanburugu/Desktop/DAEN 690/Industries/milk butter and dried milk products (09)/Natural_Foods_Whole_Milk_Powder.pdf'

# Open the file in binary mode
with open(file_path_milk_dried_prods_09, 'rb') as pdf_file:
    
    # Define the files parameter as a dictionary
    # The key is the name of the form field for file upload (e.g., 'file')
    # The value is a tuple consisting of:
    # - The filename (or you can set it as None)
    # - The file object
    files = {'file': (file_path_milk_dried_prods_09.split('/')[-1], pdf_file)}

    # Send the POST request with the PDF file
    response = requests.post(url, files=files,verify=False)

# Check if the request was successful
if response.status_code == 200:
    print("File uploaded successfully")
    # Process the response if needed
    print(response.json())
else:
    print("Failed to upload the file")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
