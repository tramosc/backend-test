from fastapi import FastAPI
from app.modules.users.infrastructure.routers import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI + Poetry!"}

app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desarrollo; restringe esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)