
from app.services.llm_service import ask_llm

def test_llm_quality():
    context = {
        "transcript": "This is a test document about artificial intelligence. AI is transforming the world.",
        "language": "en"
    }
    question = "What is this document about?"
    
    print("Generating response...")
    response = ask_llm(context, question)
    print(f"\nQuestion: {question}")
    print(f"Response:\n{response}")

if __name__ == "__main__":
    test_llm_quality()
