from fastapi import FastAPI,File,UploadFile,Header,HTTPException
from pipeline.pipeline import KnowledgePipeline
from pipeline.store import current_version
app=FastAPI(title="AI Knowledge Base Release Pipeline",version="1.0.0")
pipeline=KnowledgePipeline()
LEVEL={"viewer":0,"editor":1,"release-manager":2,"admin":3}
def authorize(role,required):
    if LEVEL.get(role,-1)<LEVEL[required]: raise HTTPException(status_code=403,detail="unauthorized")
@app.get("/")
def health(): return {"status":"ok","active_version":current_version()}
@app.post("/ingest")
async def ingest(file:UploadFile=File(...),x_role: str=Header(default="viewer")):
    authorize(x_role,"editor"); return pipeline.ingest(file.filename or "document.txt",await file.read())
@app.post("/release")
def release(x_role: str=Header(default="viewer")): authorize(x_role,"release-manager"); return pipeline.release()
@app.post("/retry")
def retry(x_role: str=Header(default="viewer")): authorize(x_role,"release-manager"); return pipeline.retries()
@app.get("/metrics")
def metrics(x_role: str=Header(default="viewer")): authorize(x_role,"viewer"); return pipeline.metrics()