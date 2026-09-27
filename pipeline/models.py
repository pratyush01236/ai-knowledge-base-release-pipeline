from dataclasses import dataclass,field
from typing import Optional
@dataclass
class TestReport:
    passed: bool
    accuracy: float
    grounding: float
    confidence: float
    failures: list[str]=field(default_factory=list)
@dataclass
class UpdateResult:
    status: str
    version: Optional[int]=None
    message: str=""