import httpx

def main():
    url = "http://0.0.0.0:8000/chat"
    # Updated payload to include 'sessionId' and 'usertoken'
    payload = {
        "query": "What was my first question to you?",
        "sessionId": "12345",  # Replace with actual session ID
        "usertoken": "abcde-token"  # Replace with actual user token
    }

    # Sending a POST request and handling the stream
    with httpx.stream("POST", url, json=payload, timeout=120.0) as response:  # Increased timeout
        for chunk in response.iter_text():
            print(chunk, end="", flush=True)

if __name__ == "__main__":
    main()
