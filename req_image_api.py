'''
Description:  直接调用image的api效果测试。
Author: Puyol lee
Date: 2025-04-03 06:33:44
'''
import base64
import requests
import os
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# Path to your image
image_path = "./data/image6.jpeg"

# Getting the base64 string
base64_image = encode_image(image_path)

api_key="GcQX1IjolKz9o4VO7ta2VPzOvgWwbWtN"
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{base64_image}" 
    }
)
print(ocr_response.pages[0])