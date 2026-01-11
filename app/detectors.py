import re 
from typing import List, Dict, Any, Tuple
def detect_pii(text: str) -> Tuple[str, List[str]]:
    tags=[]
    sanitized_text = text
    email_pattern=r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if re.search(email_pattern, text):
        tags.append("pii_email")
        sanitized_text = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    if re.search(phone_pattern, sanitized_text):
        tags.append("pii_phone")
    sanitized_text = re.sub(phone_pattern, "[REDACTED_PHONE]", sanitized_text)  
    return sanitized_text, tags 

def rag_injection(context_docs):
    findings = []
    bad_phrases = ["system:", "system prompt:", "ignore all previous", "ignore guidelines",
     "override policy", "override instructions", "forget everything", "act as dan", 
     "become dan", "no restrictions", "bypass restrictions", "disregard prior rules",
     "delete history", "print security keys", "how to hack ai", "how to hack ai system", "hack this website"]
    
    safe_words = ["teacher", "tutor", "professor", "explain", "teach me", "help me learn", "step by step", "like i'm 5", "for beginners"]
    
    for doc in context_docs:
        text = doc.get("text", "").lower()
        doc_id = doc.get("id", "unknown")    
        found_bad = False
        for phrase in bad_phrases:
            if phrase in text:
                findings.append({"tag": "rag_injection", "doc_id": doc_id, "evidence": f"found dangerous phrase: {phrase}" })
                found_bad = True
                break  
        if not found_bad and "act as" in text:
            is_learning = False
            for word in safe_words:
                if word in text:
                    is_learning = True
                    break
            if not is_learning:
                findings.append({ "tag": "rag_injection", "doc_id": doc_id, "evidence": "suspicious 'act as' without learning context"})
    return findings

def prompt_injection(prompt:str) -> List[Dict[str,str]]:
    findings = []
    text = prompt.lower()
    dangerous = [
        "ignore previous instructions", "ignore all previous", "disregard previous", 
        "forget previous instructions", "reveal your system prompt", "show me your system prompt",
        "act as dan", "you are now dan", "become dan", "developer mode", "unrestricted mode", 
        "bypass restrictions", "no restrictions", "god mode", "jailbreak me",
        "how to hack you", "exploit vulnerability", "sql injection", "execute code", "bypass security",
        "how to hack ai", "how to hack ai system", "hack this website"]
    for phrase in dangerous:
        if phrase in text:
            findings.append({
                "tag": "prompt_injection",
                "evidence": f"matched: '{phrase}'"
            })
            break  
    return findings