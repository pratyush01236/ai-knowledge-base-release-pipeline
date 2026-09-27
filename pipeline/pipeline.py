import time
from .evaluator import evaluate
from .monitor import Monitor
from .scheduler import in_window,retry_plan
from .security import contains_prompt_injection
from .store import activate,current_version,ingest_file,quarantine,rollback,snapshot
class KnowledgePipeline:
    def __init__(self): self.monitor=Monitor()
    def ingest(self,filename,data):
        text=data.decode("utf-8",errors="replace")
        if contains_prompt_injection(text): return quarantine(filename,data,"prompt injection detected")
        return ingest_file(filename,data)
    def release(self):
        docs=[d for d in snapshot()["documents"].values() if d["status"]=="candidate"]
        if not docs: return {"status":"no_change"}
        report=evaluate(docs)
        if not report.passed: return {"status":"rejected","reason":"quality gate failed","report":report.__dict__,"retry_delays_minutes":retry_plan()}
        if not in_window(): return {"status":"approved_waiting","message":"Approved update waits for maintenance window.","version":max(d["version"] for d in docs)}
        previous=current_version(); version=max(d["version"] for d in docs); start=time.time(); activate(version)
        healthy=self.monitor.health()
        if not healthy: rollback(previous); return {"status":"rolled_back","previous_version":previous,"reason":"health check failed within rollback window"}
        return {"status":"activated","version":version,"previous_version":previous,"latency_ms":int((time.time()-start)*1000)}
    def retries(self): return {"status":"retry_scheduled","after_minutes":retry_plan()}
    def metrics(self): return self.monitor.public()