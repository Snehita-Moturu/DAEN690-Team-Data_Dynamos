import requests
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>Enter Image URL to Get FDA Code</h2>
    <input type="text" id="image_url" placeholder="Enter Image URL">
    <button onclick="getFDAcode()">Get FDA Code</button>
    <div id="fda_code"></div>
    
    <script>
    function getFDAcode() {
        var imageUrl = document.getElementById('image_url').value;
        fetch('/get_fda_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({image_url: imageUrl}),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('fda_code').innerText = 'FDA Code: ' + data.fda_code;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    </script>
    '''

@app.route('/get_fda_code', methods=['POST'])
def get_fda_code():
    data = request.get_json()
    image_url = data['image_url']
    FDA_code = get_FDA_code_from_image_url(image_url)  # Ensure this function is correctly implemented
    return jsonify({'fda_code': FDA_code})


# Function to make API requests with authorization headers
def make_api_request(url, params=None):
    # Authorization credentials
    authorization_user = 'vbothra@gmu.edu'
    authorization_key = 'M7TbjKUUq675s6XV'
    headers = {
        'Authorization-User': authorization_user,
        'Authorization-Key': authorization_key,
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_FDA_code_from_image_url(image_url):
    
    
    # Signature
    signature = '6rIcb'

    # API URL for industry data
    industry_url = 'https://www.accessdata.fda.gov/rest/pcbapi/v1/industry'

    # API URL for class data
    class_url = 'https://www.accessdata.fda.gov/rest/pcbapi/v1/class'
    
    # API URL for subclass data
    subclass_url = 'https://www.accessdata.fda.gov/rest/pcbapi/v1/subclass'
    
    # API URL for PIC data
    pic_url = 'https://www.accessdata.fda.gov/rest/pcbapi/v1/pic'
    # Openai Key
    openai.api_key="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"
    
    # Fetch industry data
    industry_data = make_api_request(industry_url, params={'signature': signature})
    # print("Industry Data:", industry_data)
    
    # Fetch class data
    class_data = make_api_request(class_url, params={'signature': signature})
    # print("Class Data:", class_data)
    
    # Fetch subclass data
    subclass_data = make_api_request(subclass_url, params={'signature': signature})
    # print("Subclass Data:", subclass_data)
    
    # Fetch PIC data
    pic_data = make_api_request(pic_url, params={'signature': signature})
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
                            "url": image_url
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
                        "url": image_url
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
                            "url": image_url
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
                            "url": image_url
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
    FDA_code = response_industry.choices[0].message.content + " " + response_class.choices[0].message.content + " " + response_subclass.choices[0].message.content + " " + response_PIC.choices[0].message.content

    return FDA_code

if __name__ == '__main__':
    app.run(debug=True)