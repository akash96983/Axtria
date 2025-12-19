import logging
import os

# Ensure log directory exists
os.makedirs("backend_logs", exist_ok=True) 

logging.basicConfig(
    filename="backend_logs/chat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_interaction(query: str, response: dict):
    source = response.get('source') if response else "None"
    status = response.get('status', 'unknown')
    logging.info(f"Query: {query} | Source: {source} | Status: {status}")
    print(f"Logged: {query} -> {source}")
