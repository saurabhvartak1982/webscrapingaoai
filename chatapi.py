from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from llmchatbot import Chatbot  # Import the Chatbot class from chatbot.py

# Initialize FastAPI app
app = FastAPI()

# Initialize the chatbot
chatbot = Chatbot()

@app.post("/chat")
async def chat(request: Request):
    # Extract user query from the request body
    body = await request.json()
    user_query = body.get('query', '')

    # Define a generator function to stream responses
    def generate_response():
        for chunk in chatbot.get_response(user_query):
            yield chunk

    # Stream the chatbot's response using StreamingResponse
    return StreamingResponse(generate_response(), media_type="text/plain")
