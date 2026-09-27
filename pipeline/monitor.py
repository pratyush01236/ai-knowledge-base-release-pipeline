class Monitor:
    def __init__(self): self.metrics={"latency_ms":[],"failures":0,"confidence":[],"escalations":0}
    def record(self,latency_ms,confidence,failed=False,escalation=False):
        self.metrics["latency_ms"].append(latency_ms); self.metrics["confidence"].append(confidence); self.metrics["failures"]+=int(failed); self.metrics["escalations"]+=int(escalation)
    def health(self,max_latency_ms=3000):
        a=self.metrics["latency_ms"]; return not a or sum(a[-10:])/len(a[-10:])<=max_latency_ms
    def public(self): return self.metrics.copy()