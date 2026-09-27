from .models import TestReport
from .security import contains_prompt_injection
def evaluate(documents,baseline_accuracy=0.90,baseline_grounding=0.90):
    failures=[]; total=max(1,len(documents)); clean=0
    for d in documents:
        if contains_prompt_injection(d["text"]): failures.append("prompt injection: "+d["source"])
        elif d["text"].strip(): clean+=1
    accuracy=clean/total; grounding=clean/total
    passed=not failures and accuracy>=baseline_accuracy and grounding>=baseline_grounding
    return TestReport(passed,accuracy,grounding,min(accuracy,grounding),failures)