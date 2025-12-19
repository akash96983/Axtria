INTENT_SYNONYMS = {
    "adverse_events": ["ae", "aes", "side effect", "adverse", "reaction", "toxicity", "reaction"],
    "dosage": ["dose", "dosage", "frequency", "administer", "amount", "mg", "pill", "mg/kg", "q3w", "daily"],
    "label_info": [
        "label", "warning", "precaution", "caution", "guidance", "risk", 
        "monitor", "careful", "context", "background", "summary", "notes"
    ],
    "indication": ["indication", "treat", "purpose", "disease", "condition", "intended for", "prophylaxis"],
    "population": ["population", "adult", "pediatric", "child", "age", "group"],
    "severity": ["severity", "serious", "moderate", "mild", "severe", "grade"],
    "outcome": ["outcome", "status", "result", "ongoing", "resolved", "fatal"]
}

def normalize_query(text):
    t = text.lower()
    intents = set()

    for intent, words in INTENT_SYNONYMS.items():
        for w in words:
            # Simple keyword matching
            if w in t:
                intents.add(intent)

    return intents
