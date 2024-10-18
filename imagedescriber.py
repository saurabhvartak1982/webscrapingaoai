import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Function to call Azure OpenAI and describe an image URL
def describe_image(image_url):

    client = AzureOpenAI(
        base_url=f"{os.getenv('AZURE_OPENAI_ENDPOINT_VISION')}/openai/deployments/{os.getenv('AZURE_LLM_DEPLOYMENT_VISION')}", 
        api_key=os.getenv("AZURE_OPENAI_API_KEY_VISION"),  
        api_version=os.getenv("AZURE_OPENAI_API_VERSION_VISION")
        )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_LLM_DEPLOYMENT_VISION"),
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture directly without using the words - this picture shows ... or .. this image captures:" 
                    
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": f"{image_url}"
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )

    return response
