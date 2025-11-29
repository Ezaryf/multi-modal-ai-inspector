"""
LLM service for conversational analysis
Using small local models for zero-cost deployment
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os
from typing import Dict, List

# Global models (lazy loaded)
_llm_pipeline = None

def get_llm_pipeline():
    """Lazy load LLM pipeline"""
    global _llm_pipeline
    if _llm_pipeline is None:
        model_name = os.getenv("LLM_MODEL", "facebook/opt-1.3b")
        print(f"Loading LLM model: {model_name}")
        
        _llm_pipeline = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            device=-1,  # CPU
            max_length=512
        )
    return _llm_pipeline

SYSTEM_PROMPT = """You are "Inspector": an AI analyst assistant. 
When answering questions about media:
1. First provide a 3-bullet structured summary (facts only)
2. Then give one creative paragraph reading of the media
3. Provide explicit source pointers (transcript timestamps, frame indexes)
4. If unsure, say "I might be mistaken" and point to the source

Keep responses concise and factual."""

def ask_llm(context: Dict, question: str, chat_history: List[Dict] = None) -> str:
    """
    Generate response using LLM with context
    
    Args:
        context: Analysis results (transcript, captions, etc.)
        question: User's question
        chat_history: Previous chat messages
    
    Returns: LLM response
    """
    # Build prompt with context
    prompt = build_prompt(context, question, chat_history)
    
    # Generate response
    llm = get_llm_pipeline()
    
    try:
        result = llm(
            prompt,
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1
        )
        
        # Extract generated text
        generated = result[0]["generated_text"]
        
        # Remove the prompt part
        response = generated[len(prompt):].strip()
        
        return response
    except Exception as e:
        print(f"LLM generation failed: {e}")
        return generate_fallback_response(context, question)

def build_prompt(context: Dict, question: str, chat_history: List[Dict] = None) -> str:
    """Build prompt with context and question"""
    
    # Extract relevant context
    facts = []
    
    if "caption" in context:
        facts.append(f"- Image caption: {context['caption']}")
    
    if "transcript" in context:
        transcript = context["transcript"][:500]  # Limit length
        facts.append(f"- Transcript excerpt: {transcript}")
    
    if "sentiment" in context:
        sent = context["sentiment"]
        facts.append(f"- Sentiment: {sent.get('label', 'unknown')} (confidence: {sent.get('score', 0)})")
    
    if "visual_summary" in context:
        facts.append(f"- Visual summary: {context['visual_summary']}")
    
    if "language" in context:
        facts.append(f"- Language: {context['language']}")
    
    # Build conversation history
    history_text = ""
    if chat_history:
        for msg in chat_history[-3:]:  # Last 3 messages
            role = msg.get("role", "user")
            text = msg.get("message", "")
            history_text += f"{role.upper()}: {text}\n"
    
    # Construct final prompt
    prompt = f"""{SYSTEM_PROMPT}

CONTEXT:
{chr(10).join(facts) if facts else "No context available"}

{history_text}
USER: {question}
ASSISTANT:"""
    
    return prompt

def generate_fallback_response(context: Dict, question: str) -> str:
    """Generate simple fallback response when LLM fails"""
    facts = []
    
    if "caption" in context:
        facts.append(f"The image shows: {context['caption']}")
    
    if "transcript" in context:
        facts.append(f"Transcript: {context['transcript'][:200]}...")
    
    if "sentiment" in context:
        facts.append(f"Overall sentiment: {context['sentiment'].get('label', 'unknown')}")
    
    return "\n".join(facts) if facts else "I couldn't analyze this media properly."

def summarize_analysis(analysis: Dict) -> str:
    """Generate summary report from analysis"""
    prompt = f"""Summarize this media analysis in 2-3 sentences:

{str(analysis)}

Summary:"""
    
    llm = get_llm_pipeline()
    
    try:
        result = llm(prompt, max_new_tokens=150, temperature=0.7)
        generated = result[0]["generated_text"]
        summary = generated[len(prompt):].strip()
        return summary
    except:
        return "Analysis completed. Ask questions to explore the content."
