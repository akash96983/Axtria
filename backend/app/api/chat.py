from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services import query_router, logger_service, context_store
import os

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query_text = request.text
    session_id = request.session_id
    
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text is required")

    # Route and retrieve with session context
    result = query_router.route_query(query_text, session_id)
    
    # Construct response
    if result:
        response_data = {
            "text": result["text"],
            "source": result["source"],
            "count": result["count"],
            "status": result.get("status", "success")
        }
        
        # Step 6: Update Context After Successful Answer
        if result.get("status") == "success" and "meta" in result:
             meta = result["meta"]
             context_store.update_context(
                 session_id,
                 drug=meta.get("drug"),
                 intent=meta.get("intent"),
                 source=meta.get("source")
             )
             
    else:
        response_data = {
            "text": "I could not find specific records matching your query in the available documents. Please verify the drug name or trial phase.",
            "source": None,
            "count": 0,
            "status": "no_content"
        }

    # Log interaction
    logger_service.log_interaction(query_text, response_data)
    
    return response_data

@router.get("/logs")
async def get_logs():
    log_file_path = "backend_logs/chat.log"
    logs = []
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r") as f:
                # Read lines in reverse order (newest first)
                lines = f.readlines()[::-1]
                for i, line in enumerate(lines):
                    if not line.strip(): continue
                    # Parse simple log format: timestamp - level - message
                    # Message format: Query: {q} | Source: {s} | Status: {st}
                    parts = line.split(" - ", 2)
                    if len(parts) >= 3:
                        msg_part = parts[2]
                        if "|" in msg_part:
                            q_part, s_part, st_part = msg_part.split("|")
                            logs.append({
                                "id": i,
                                "turn": len(lines) - i,
                                "timestamp": parts[0],
                                "query": q_part.replace("Query:", "").strip(),
                                "source": s_part.replace("Source:", "").strip(),
                                "status": st_part.replace("Status:", "").strip()
                            })
        except Exception as e:
            print(f"Error reading logs: {e}")
            
    return logs[:50] # Return last 50 logs
