import httpx
# import time

def main():
    url = "http://<your-server>/chat"
    payload = {"query": "Write 10 lines on Mumbai"}

    # Sending a POST request and handling the stream
    with httpx.stream("POST", url, json=payload, timeout=60.0) as response:
        for chunk in response.iter_text():
            print(chunk, end="", flush=True)
            # time.sleep(0.1)

if __name__ == "__main__":
    main()
