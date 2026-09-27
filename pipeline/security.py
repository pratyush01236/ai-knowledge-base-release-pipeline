import re
from pathlib import Path
INJECTION_PATTERNS=[r"ignore\s+(all\s+)?previous\s+instructions",r"ignore\s+(the\s+)?system\s+prompt",r"reveal\s+(the\s+)?system\s+prompt",r"developer\s+message",r"follow\s+these\s+instructions\s+instead",r"disregard\s+security"]
SENSITIVE=[(re.compile(r"\b(?:\d[ -]?){13,19}\b"),"[CARD_REDACTED]"),(re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",re.I),"[EMAIL_REDACTED]"),(re.compile(r"\b(?:\+?\d[\d ()-]{8,}\d)\b"),"[PHONE_REDACTED]")]
def contains_prompt_injection(text):
    return any(re.search(p,text or "",re.I) for p in INJECTION_PATTERNS)
def mask_sensitive(text):
    out=text or ""
    for pattern,replacement in SENSITIVE: out=pattern.sub(replacement,out)
    return out
def safe_filename(name): return Path(name).name