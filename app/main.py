from fastapi import FastAPI
from app.routers import auth, users, projects, tasks, admin

app = FastAPI(title= "TaskFlow API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"status": "ok"}
