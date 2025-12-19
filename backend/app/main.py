from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
import uvicorn

app = FastAPI(title="Clinical Trial Query Chatbot API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for demo, in prod restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Clinical Trial Query Chatbot Backend is running"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
