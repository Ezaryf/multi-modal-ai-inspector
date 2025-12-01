
def test_truncation():
    # Simulate a bad response from the LLM
    prompt = "PROMPT"
    generated_text = "PROMPT This is a good answer. USER: What is next? ASSISTANT: I don't know."
    
    # Logic from llm_service.py
    response = generated_text[len(prompt):].strip()
    
    stop_tokens = ["USER:", "ASSISTANT:", "User:", "Assistant:"]
    for token in stop_tokens:
        if token in response:
            response = response.split(token)[0].strip()
            
    print(f"Original: '{generated_text}'")
    print(f"Processed: '{response}'")
    
    assert response == "This is a good answer."
    print("✅ Truncation test passed!")

if __name__ == "__main__":
    test_truncation()
