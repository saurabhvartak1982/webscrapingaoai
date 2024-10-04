# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
COPY chatapi.py /app
COPY llmchatbot.py /app
COPY .env /app

# Install any needed packages specified in requirements.txt
# Note: Make sure you have a requirements.txt file at the same directory level as your Dockerfile
# Your requirements.txt should include fastapi, uvicorn, python-dotenv, tiktoken, openai, and any other dependencies your app needs
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
# Note: Ensure you have gunicorn or uvicorn installed in your requirements.txt for running FastAPI
CMD ["uvicorn", "chatapi:app", "--host", "0.0.0.0", "--port", "8000"]