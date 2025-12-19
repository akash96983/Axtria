import json
import os

DB_FILE = "context_db.json"
SESSION_CONTEXT = {}

def load_db():
    global SESSION_CONTEXT
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                SESSION_CONTEXT = json.load(f)
        except:
            SESSION_CONTEXT = {}

def save_db():
    try:
        with open(DB_FILE, "w") as f:
            json.dump(SESSION_CONTEXT, f)
    except Exception as e:
        print(f"Error saving DB: {e}")

# Initial load
load_db()

def get_context(session_id: str):
    load_db() 
    return SESSION_CONTEXT.get(session_id, {})

def update_context(session_id: str, drug=None, intent=None, source=None):
    load_db()
    if session_id not in SESSION_CONTEXT:
        SESSION_CONTEXT[session_id] = {}

    if drug:
        SESSION_CONTEXT[session_id]["drug"] = drug
    if intent is not None: 
        SESSION_CONTEXT[session_id]["intent"] = intent
    if source:
        SESSION_CONTEXT[session_id]["source"] = source
    
    save_db()
        
def clear_context(session_id: str):
    if session_id in SESSION_CONTEXT:
        del SESSION_CONTEXT[session_id]
