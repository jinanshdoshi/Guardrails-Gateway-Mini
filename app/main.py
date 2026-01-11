from fastapi import FastAPI, HTTPException
from app.models import AnalysisRequest, AnalysisResponse, PolicyResponse, ContextDoc
from app.detectors import detect_pii, prompt_injection, rag_injection

app = FastAPI(title="SentraGuard Lite")

@app.get("/policy", response_model=PolicyResponse)
def get_policy():
    return {
        "version": "1.0",
        "detectors": ["pii_email", "pii_phone", "prompt_injection", "rag_injection"],
        "thresholds": {"block_score": 80, "transform_score": 40}
    }

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_request(request: AnalysisRequest):
    sanitized_prompt, pii_tags = detect_pii(request.prompt)
    injection_findings = prompt_injection(request.prompt)
    rag_findings = rag_injection(request.context_docs)
    rag_evidence = []
    rag_tags = []
    for f in rag_findings:
        rag_tags.append(f["tag"])
        rag_evidence.append({"tag": f["tag"], "evidence": f["evidence"]})
    injection_tags = []
    injection_evidence = []
    for f in injection_findings:
        injection_tags.append(f["tag"])
        injection_evidence.append({"tag": f["tag"], "evidence": f["evidence"]})

    all_tags = pii_tags + injection_tags + list(set(rag_tags))
    all_reasons = rag_evidence + injection_evidence
    score = 0
    
    if "prompt_injection" in all_tags:
        score += 80
    if "rag_injection" in all_tags:
        score += 80
    if "pii_email" in all_tags or "pii_phone" in all_tags:
        score += 40
        
    score = min(score, 100) 

    decision = "allow"
    if score >= 80:
        decision = "block"
    elif score >= 40:
        decision = "transform"

    return {
        "decision": decision,
        "risk_score": score,
        "risk_tags": sorted(list(set(all_tags))),
        "sanitized_prompt": sanitized_prompt if decision != "block" else None,
        "sanitized_context_docs": request.context_docs,
        "reasons": all_reasons
    }