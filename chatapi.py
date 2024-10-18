from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llmchatbot import Chatbot  # Import the Chatbot class from chatbot.py

# Initialize FastAPI app
app = FastAPI()

# Initialize the chatbot
chatbot = Chatbot()

# Define a Pydantic model for the request body
class ChatRequest(BaseModel):
    query: str
    sessionId: str
    usertoken: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Extract the values from the Pydantic model
    user_query = request.query
    session_id = request.sessionId
    user_token = request.usertoken

    # Define a generator function to stream responses
    async def generate_response():
        async for chunk in chatbot.get_response(user_query, session_id, user_token):
            yield chunk

    # Stream the chatbot's response using StreamingResponse
    return StreamingResponse(generate_response(), media_type="text/plain")
