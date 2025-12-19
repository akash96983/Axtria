from app.services import retriever_excel

def test_retrieval():
    print("Testing retrieve_excel...")
    try:
        data, conf = retriever_excel.retrieve_excel("Metformin", {"dosage"})
        print(f"Result: {data}")
        print(f"Confidence: {conf}")
        
        if conf == 1:
            print("SUCCESS")
        else:
            print("FAILURE")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    test_retrieval()
