from app.services import retriever_excel, retriever_doc, normalizer, context_store, followup_detector

# Layer 0: Safety Guardrails
def check_safety(text: str):
    text_lower = text.lower()
    # Keywords that imply medical advice or prescriptive actions
    unsafe_triggers = [
        "prescribe", "my patient", "what should i do", "treatment plan",
        "dosage adjustment recommendations", "clinical advice", "recommend for me",
        "safe for", "safety of", "better", "best drug", "compare", "opinion",
        "safe in", "contraindication"
    ]
    
    # Check for direct safety questions "Is X safe?"
    if "safe" in text_lower and (" for " in text_lower or " in " in text_lower):
         return {
            "text": "I cannot provide medical advice or safety assessments for specific patient populations. Please consult the official product label or a qualified healthcare professional.",
            "source": "System (Safety Guardrail)",
            "count": 0,
            "status": "refusal"
        }
    
    if any(trigger in text_lower for trigger in unsafe_triggers):
        return {
            "text": "I cannot provide medical advice or prescriptive recommendations. Please consult the official product label or a qualified healthcare professional.",
            "source": "System (Safety Guardrail)",
            "count": 0,
            "status": "refusal"
        }
    return None

def route_query(text: str, session_id: str = "default"):
    # Layer 0: Safety Check
    safety_response = check_safety(text)
    if safety_response:
        return safety_response

    # Layer 1: Normalization
    intents = normalizer.normalize_query(text)
    
    # Layer 2: Identify Drug (Context-Aware)
    # Check for general terms first to avoid using stale context
    general_terms = ["checkpoint inhibitor", "targeted therap", "clinical context", "trial summary", "ae severity"]
    is_general = any(term in text.lower() for term in general_terms)
    
    drug_name = retriever_excel.find_drug_name(text)
    
    context = context_store.get_context(session_id)

    # Follow-up Resolution (Cleaned)
    if not drug_name and not is_general:
        if intents and context.get("drug"):
             drug_name = context.get("drug")
        elif followup_detector.is_follow_up(text) and context.get("drug"):
             drug_name = context.get("drug")

    # If still no drug found, we must clarify (unless general doc search is intended)
    if not drug_name:
        # Allow broad search for clinical context, general AE types, or outcomes
        broad_search_intents = {"label_info", "adverse_events", "outcome"}
        if any(intent in broad_search_intents for intent in intents):
             # Try broad doc search for background info
             res, conf = retriever_doc.retrieve_doc("", intents)
             if conf > 0: return res
             
        # Check for general keywords if no specific drug
        if any(k in text.lower() for k in ["checkpoint inhibitor", "targeted therapy", "clinical context", "severity", "category"]):
             res, conf = retriever_doc.retrieve_doc("", intents)
             if conf > 0: return res

        return {
            "text": "Could you please specify which drug you are referring to? I couldn't find a drug name in your query or previous context.",
            "source": "System",
            "count": 0,
            "status": "clarification_needed"
        }

    # Decide primary source
    score_excel = 0
    score_doc = 0

    if "adverse_events" in intents: score_excel += 1
    if "dosage" in intents: score_excel += 2
    if "indication" in intents: score_excel += 1 
    if "outcome" in intents: score_excel += 1
    
    # Doc gets high priority for warnings/cautions
    if "label_info" in intents: score_doc += 5 
    
    # Keyword check in raw text for routing hints
    raw_lower = text.lower()
    if any(k in raw_lower for k in [
        "caution", "warning", "monitoring", "label", "guidance", "risk", 
        "note", "cardiotoxicity", "toxicity", "describe", "report", "summary"
    ]):
        score_doc += 5

    # Mixed Intent Check (If user asks for data AND label)
    if score_excel > 0 and score_doc > 5:
        res_excel, conf_excel = retriever_excel.retrieve_excel(drug_name, intents)
        res_doc, conf_doc = retriever_doc.retrieve_doc(drug_name, intents)
        
        if conf_excel > 0 and conf_doc > 0:
            combined_text = f"{res_excel['text']}\n\n[Label & Safety Notes]:\n{res_doc['text']}"
            return {
                "text": combined_text,
                "source": "Pharma_Clinical_Trial_AllDrugs.xlsx, Pharma_Clinical_Trial_Notes.docx",
                "count": res_excel["count"] + res_doc["count"],
                "status": "success"
            }

    primary_source = "excel"
    if score_doc > score_excel:
        primary_source = "doc"
        
    # Layer 3 & 4: Retrieval & Cross-Check
    if primary_source == "excel":
        result, confidence = retriever_excel.retrieve_excel(drug_name, intents)
        if confidence > 0:
            result["meta"] = {"drug": drug_name, "intent": list(intents), "source": "excel"}
            return result
        # Fallback to Doc
        result, confidence = retriever_doc.retrieve_doc(drug_name, intents)
        if confidence > 0:
            result["meta"] = {"drug": drug_name, "intent": list(intents), "source": "doc"}
            return result
            
    else: # primary_doc
        result, confidence = retriever_doc.retrieve_doc(drug_name, intents)
        if confidence > 0:
            result["meta"] = {"drug": drug_name, "intent": list(intents), "source": "doc"}
            return result
        # Fallback to Excel
        result, confidence = retriever_excel.retrieve_excel(drug_name, intents)
        if confidence > 0:
            result["meta"] = {"drug": drug_name, "intent": list(intents), "source": "excel"}
            return result

    # If both fail
    return {
        "text": f"I couldn't confidently determine whether this refers to dosing data or label information for {drug_name}. Could you please clarify?",
        "source": "System",
        "count": 0,
        "status": "unknown"
    }
