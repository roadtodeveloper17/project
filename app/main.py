from fastapi import FastAPI

app = FastAPI(title= "TaskFlow API")

@app.get("/health")
def health():
    return {"status": "ok"}
