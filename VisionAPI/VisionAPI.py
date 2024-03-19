import requests


# Authorization credentials
authorization_user = 'vbothra@gmu.edu'
authorization_key = 'M7TbjKUUq675s6XV'

# API URL for subclass data
subclass_url = 'https://www.accessdata.fda.gov/rest/pcbapi/v1/subclass'

# Signature
signature = '6rIcb'

# Function to make API requests with authorization headers
def make_api_request(url, params=None):
    headers = {
        'Authorization-User': authorization_user,
        'Authorization-Key': authorization_key,
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Fetch subclass data
subclass_data = make_api_request(subclass_url, params={'signature': signature})
print("Subclass Data:", subclass_data)


import openai

openai.api_key="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"

response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": f"Can you tell the container packing type of this product in the image? and categorize the container type based on the following subclass data from FDA {subclass_data}",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://m.media-amazon.com/images/I/61UOnm0u0nL._SX569_PIbundle-24,TopRight,0,0_AA569SH20_.jpg"
                    },
                },
            ],
        }
    ],
    max_tokens=400,
)

print(response.choices[0].message.content)