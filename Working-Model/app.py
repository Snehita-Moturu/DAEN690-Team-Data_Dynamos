import requests
import openai
from flask import Flask, request, jsonify,render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_fda_code', methods=['POST'])
def get_fda_code():
    data = request.get_json()
    image_base64 = data['image_base64']
    include_subclass = data.get('include_subclass', True)  # Include subclass by default

    FDA_code = get_FDA_code_from_image_base64(image_base64, include_subclass)
    return jsonify(FDA_code)

def get_FDA_code_from_image_base64(image_base64, include_subclass=True):
    # Encode the image
    image_data = f"data:image/jpeg;base64,{image_base64}"
    
    # Openai Key
    openai.api_key="apikeyhere"
    
    # Fetch industry data
    industry_csv_file_path = "/Users/saisharanburugu/Downloads/Test 3/industry_api_result_data.csv"
    industry_csv = pd.read_csv(industry_csv_file_path)
    industry_data = industry_csv.to_json(orient='records')
    # print("Industry Data:", industry_data)
    
    # Fetch class data
    class_csv_file_path = "/Users/saisharanburugu/Downloads/Test 3/class_api_result_data.csv"
    class_csv = pd.read_csv(class_csv_file_path)
    class_data = class_csv.to_json(orient='records')
    # print("Class Data:", class_data)
    
    # Fetch subclass data
    subclass_csv_file_path = "/Users/saisharanburugu/Downloads/Test 3/subclass_api_result_data.csv"
    subclass_csv = pd.read_csv(subclass_csv_file_path)
    subclass_data = subclass_csv.to_json(orient='records')
    # print("Subclass Data:", subclass_data)
    
    # Fetch PIC data
    pic_csv_file_path = "/Users/saisharanburugu/Downloads/Test 3/pic_api_result_data.csv"
    pic_csv = pd.read_csv(pic_csv_file_path)
    pic_data = pic_csv.to_json(orient='records')
    # print("PIC Data:", pic_data)
 
    # Prompt to get the industry code according to FDA codes.
    response_industry = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": f"Can you tell the industry code of this product in the image? and categorize the industry based on the following industry data from FDA {industry_data}"
                        "Don't give a detailed description just give me the industry code i dont want any sentences just output the industry code",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": image_data
                            },
                            },
                            ],
                            }
                            ],
        max_tokens=400,
        )

    # Prompt to get the class code according to FDA codes.
    response_class = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {   
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": f"Can you tell the class of this product in the image? and categorize the class based on the following class data from FDA {class_data}"
                        "Don't give a detailed description just give me the class code i dont want any sentences just output the class code the json file contains three things industry id, classid and class description all three are in the following order and i just want class id as output and the class id is like industry-classcode I just want the alphabet for example if class id is like 29-B or 29B I just want B where B is the class id",
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data
                        },
                        },
                        ],
                        }
                        ],
        max_tokens=400,
        )

    # Prompt to get the subclass code according to FDA codes.
    response_subclass = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": f"Can you tell the container packing type of this product in the image? and categorize the container type based on the following subclass data from FDA {subclass_data}"
                        "Don't give a detailed description just give me the code i dont want any sentences just output the subclass code in the json file it has three things subclassid, subclasscode and subclass description all three in the same order i just want subclasscode in the output.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data
                        },
                        },
                        ],
                        }
                        ],
        max_tokens=400,
        ) 

    # Prompt to get the PIC code according to FDA codes.
    response_PIC = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": """Based on this description The Process Indicator Code describes the process used in preparing a food product. 
                        There are 14 possible processes to choose from. The first decision to be made is whether a product is Unprocessed (Raw) or Processed (Packaged). 
                        The invoice or other product information should help you determine whether the product is unprocessed or processed.
                        If the product has not been processed, the appropriate Raw PIC (i.e., B, C or D) is used. Keep in mind that Raw refers to unprocessed products (e.g., fresh, and or in natural state). 
                        If the product has received any type of processing, the Raw PICs do not apply. For example, filleted, skinned, fresh fish; peeled or deveined shrimp; or smoked fish are processed foods. One of the processed PICs should be selected.
                        The most widely used PIC for processed foods is Packaged Food. 
                        However, when appropriate, a specific PIC should be utilized to identify the treatment used in preparing the finished product, e.g., heat treated (cooked); pasteurized; commercially sterile; ultra-pasteurized; aseptic pack; or other processing used."""
                        f"Can you tell the process indicator code (PIC) of this product in the image? and categorize the process indicator code based on the following PIC data from FDA {pic_data}"
                        "Don't give a detailed description just give me the code i dont want any sentences just output the PIC code",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data
                        },
                        },
                        ],
                        }
                        ],
        max_tokens=400,
        )
    
    print("--------------------------------")
    print("The industry code of the product is "+response_industry.choices[0].message.content)
    print("The class code of the product is "+response_class.choices[0].message.content)
    print("The subclass code of the product is "+response_subclass.choices[0].message.content)
    print("The PIC code of the product is "+response_PIC.choices[0].message.content)
    print("--------------------------------")
    industry_code = response_industry.choices[0].message.content
    class_code = response_class.choices[0].message.content
    sub_class_code = response_subclass.choices[0].message.content if include_subclass else "No subclass provided"
    pic_code = response_PIC.choices[0].message.content

    if include_subclass:
        fda_code = f"{industry_code} {class_code} {sub_class_code} {pic_code}"
    else:
        fda_code = f"{industry_code} {class_code} {pic_code}"

    fda_code_data = {
        'industry': industry_code,
        'class': class_code,
        'subclass': sub_class_code,
        'PIC': pic_code ,
        'product': "Product Code Placeholder",
        'fda_code': fda_code
    }
    return fda_code_data

if __name__ == '__main__':
    app.run(debug=True)