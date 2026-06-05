from fastapi import FastAPI
from app.routers import auth, users, projects, tasks

app = FastAPI(title= "TaskFlow API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)

@app.get("/health")
def health():
    return {"status": "ok"}
