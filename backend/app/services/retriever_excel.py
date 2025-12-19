import pandas as pd
import os
from thefuzz import process

# Global cache
DF_DRUGS = None
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/Pharma_Clinical_Trial_AllDrugs.xlsx")

def load_data():
    global DF_DRUGS
    if DF_DRUGS is None:
        try:
            DF_DRUGS = pd.read_excel(DATA_PATH)
            # Normalize column names
            DF_DRUGS.columns = [c.strip() for c in DF_DRUGS.columns]
        except Exception as e:
            print(f"Error loading Excel: {e}")
            DF_DRUGS = pd.DataFrame()

def retrieve_excel(drug_name: str, intents: set):
    load_data()
    if DF_DRUGS.empty:
        return None, 0
    
    # Filter by drug
    start_confidence = 0
    
    # 1. Exact/Smart Fuzzy Match
    drugs = DF_DRUGS['drug_name'].dropna().unique().tolist()
    match = process.extractOne(drug_name, drugs)
    
    if not match or match[1] < 70:
        return None, 0
        
    actual_drug = match[0]
    
    # Filter dataframe
    record = DF_DRUGS[DF_DRUGS['drug_name'] == actual_drug].iloc[0]
    
    # Build response based on intents
    response_parts = []
    
    # 1. Indication & Population
    indication = record.get('indication', 'N/A')
    population = record.get('population', 'N/A')
    if "indication" in intents:
        response_parts.append(f"Indication: {indication} (Population: {population})")
    
    # 2. Dosage
    if "dosage" in intents:
        response_parts.append(f"Dose: {record.get('dose', 'N/A')}")
        
    # 3. Adverse Events & Severity
    ae_terms = record.get('ae_terms', 'N/A')
    severity = record.get('severity', 'N/A')
    if "adverse_events" in intents:
        response_parts.append(f"AEs: {ae_terms} (Severity: {severity})")
        
    # 4. Outcome
    outcome = record.get('outcome', 'N/A')
    if "outcome" in intents:
        response_parts.append(f"Outcome: {outcome}")
        
    # Default fallback if no specific intent matches columns but we have the drug
    if not response_parts:
         response_parts.append(f"Indication: {indication}")
         response_parts.append(f"Population: {population}")
         response_parts.append(f"Dose: {record.get('dose', 'N/A')}")
         response_parts.append(f"AEs: {ae_terms}")
         response_parts.append(f"Severity: {severity}")
         response_parts.append(f"Outcome: {outcome}")

    final_text = f"Data for {actual_drug}:\n" + "\n".join(response_parts)
    
    return {
        "text": final_text,
        "source": "Pharma_Clinical_Trial_AllDrugs.xlsx",
        "count": 1,
        "status": "success"
    }, 1 # Confidence score 1 (found record)

def find_drug_name(query: str):
    load_data()
    if DF_DRUGS.empty: return None
    
    drugs = DF_DRUGS['drug_name'].dropna().unique().tolist()
    # Find best match in query
    # This is tricky without NER, but we can iterate known drugs and check presence
    # Or rely on the previous fuzzy logic if they passed a specific name
    
    # Naive approach: Check if any known drug is substring of query
    query_lower = query.lower()
    best_drug = None
    max_len = 0
    
    for drug in drugs:
        if drug.lower() in query_lower:
            if len(drug) > max_len:
                best_drug = drug
                max_len = len(drug)
                
    return best_drug
