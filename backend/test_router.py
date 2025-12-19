from app.services import normalizer, query_router, context_store

if __name__ == "__main__":
    q = "dose"
    intents = normalizer.normalize_query(q)
    print(f"INTENTS_FOUND: {intents}")
    
    # Also check context resolution if intents found
    session_id = "test_session_123"
    ctx = context_store.get_context(session_id)
    print(f"CONTEXT_DRUG: {ctx.get('drug')}")
    
    if intents and ctx.get('drug'):
        print("IMPLICIT_LOGIC_WOULD_TRIGGER")
    
    print("Calling route_query...")
    res = query_router.route_query(q, session_id)
    print(f"ROUTER_STATUS: {res.get('status')}")
    print(f"ROUTER_TEXT: {res.get('text')[:20]}")
