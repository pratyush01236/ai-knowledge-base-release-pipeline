import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from config import KNOWLEDGE_DIR,QUARANTINE_DIR,STATE_FILE
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
def _load():
    p=Path(STATE_FILE)
    return json.loads(p.read_text()) if p.exists() else {"active_version":0,"versions":{},"documents":{}}
def _save(s): Path(STATE_FILE).write_text(json.dumps(s,indent=2))
def ingest_file(filename,data):
    state=_load(); digest=sha256_bytes(data)
    if digest in state["documents"]: return {"status":"duplicate","document":state["documents"][digest]}
    text=data.decode("utf-8",errors="replace")
    if not text.strip(): return quarantine(filename,data,"empty document")
    version=max([int(x) for x in state["versions"]] or [0])+1
    root=Path(KNOWLEDGE_DIR); root.mkdir(parents=True,exist_ok=True)
    (root/Path(filename).name).write_bytes(data)
    doc={"doc_id":digest[:16],"version":version,"sha256":digest,"source":filename,"status":"candidate","text":text,"created_at":datetime.now(timezone.utc).isoformat()}
    state["documents"][digest]=doc; _save(state); return {"status":"new","document":doc}
def quarantine(filename,data,reason):
    q=Path(QUARANTINE_DIR); q.mkdir(parents=True,exist_ok=True); (q/Path(filename).name).write_bytes(data)
    return {"status":"quarantined","reason":reason}
def current_version(): return _load()["active_version"]
def activate(version):
    s=_load(); s["active_version"]=version; s["versions"][str(version)]={"activated_at":datetime.now(timezone.utc).isoformat()}; _save(s)
def rollback(version):
    s=_load(); s["active_version"]=version; _save(s)
def snapshot(): return _load()