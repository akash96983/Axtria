import requests
import json
import time

BASE_URL = "http://localhost:8000/api/chat"
SESSION_ID = "test_session_123"

def send_message(text):
    payload = {
        "text": text,
        "session_id": SESSION_ID
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_test():
    print(f"--- Starting Context Test (Session: {SESSION_ID}) ---")
    
    # 1. First Turn: Establish Context
    print("\n1. Sending 'Metformin'...")
    res1 = send_message("Metformin")
    if res1:
        print(f"Response 1: {res1.get('text')[:100]}...")
        print(f"Status: {res1.get('status')}")
    else:
        print("Failed to get response 1")
        return

    # Short sleep to ensure backend processed update (though it's async/sync)
    time.sleep(1)

    # 2. Second Turn: Implicit Follow-up
    print("\n2. Sending 'dose'...")
    res2 = send_message("dose")
    if res2:
        print(f"Response 2: {res2.get('text')[:100]}...")
        print(f"Status: {res2.get('status')}")
        
        if res2.get("status") == "success" and "Metformin" in res2.get("text"):
            print("\nPASSED: Context logic is working!")
        else:
            print("\nFAILED: Did not retrieve Metformin dose.")
    else:
        print("Failed to get response 2")

if __name__ == "__main__":
    run_test()
