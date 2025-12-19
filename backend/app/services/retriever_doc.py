from docx import Document
import os

DOC_CACHE = None
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/Pharma_Clinical_Trial_Notes.docx")

def load_doc():
    global DOC_CACHE
    if DOC_CACHE is None:
        try:
            DOC_CACHE = Document(DATA_PATH)
        except Exception as e:
            print(f"Error loading Docx: {e}")
            DOC_CACHE = None

def retrieve_doc(drug_name: str, intents: set):
    load_doc()
    if not DOC_CACHE:
        return None, 0

    hits = []
    target_drug = drug_name.lower() if drug_name else ""
    
    # Priority words based on intents
    intent_keywords = []
    if "label_info" in intents:
        intent_keywords.extend(["warning", "caution", "label", "guidance", "monitor", "safety", "risk"])
    if "adverse_events" in intents:
        intent_keywords.extend(["adverse", "ae", "reaction", "side effect", "immune-related"])
    if "outcome" in intents:
        intent_keywords.extend(["outcome", "status", "resolved", "ongoing", "fatal"])

    for para in DOC_CACHE.paragraphs:
        text = para.text.strip()
        if not text or len(text) < 10: continue
        
        text_lower = text.lower()
        score = 0
        
        # 1. Matching Drug Name (Higher priority)
        if target_drug:
             # Very high score if paragraph is purely about the drug (starts with it or bulleted)
             if text_lower.startswith(target_drug) or f"- {target_drug}" in text_lower or f"* {target_drug}" in text_lower:
                  score += 20
             # Mentions drug but as an example in parentheses? Lower priority
             elif f"({target_drug}" in text_lower or f"(e.g., {target_drug}" in text_lower:
                  score += 5
             elif target_drug in text_lower:
                  score += 10
                  
        # 2. Match Intent Keywords
        for kw in intent_keywords:
            if kw in text_lower:
                score += 5
                
        # 3. Handle Clinical Context / Background Specifically
        is_background = any(term in text_lower for term in ["clinical context", "background info", "oncology agents like checkpoint"])
        
        # If no drug provided, background is good
        if not target_drug and is_background:
             score += 15 # Boost for general background questions
        elif target_drug and is_background:
             score -= 10 # Penalize if we have a specific drug and this is just generic background

        # General high-relevance match
        if score >= 15 or (not target_drug and score >= 10):
            hits.append({"score": score, "text": text, "is_bg": is_background})

    # Sort hits by score
    hits.sort(key=lambda x: x["score"], reverse=True)
    
    if not hits:
        return None, 0

    # Narrow down to most relevant
    top_hit = hits[0]
    final_hits = [top_hit["text"]]
    
    # If the second hit is also strong and NOT background, add it
    # OR if we have NO specific drug match, maybe keep top 2 background snippets?
    # Actually, user wants conciseness. Let's stick to 1 if top is strong.
    if len(hits) > 1 and hits[1]["score"] >= top_hit["score"] - 5:
         # Only add if it's not redundant background or if both are background
         if not hits[1]["is_bg"] or (top_hit["is_bg"] and hits[1]["is_bg"]):
              final_hits.append(hits[1]["text"])

    response_text = "\n\n".join(final_hits)
    
    return {
        "text": response_text,
        "source": "Pharma_Clinical_Trial_Notes.docx",
        "count": len(final_hits),
        "status": "success"
    }, len(final_hits)

def search_doc(query: str):
     # Backward compatibility
     res, conf = retrieve_doc("", set())
     return res
