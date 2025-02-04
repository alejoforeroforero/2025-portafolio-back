from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import app.models as models
from app.database import engine
from app.routers import profile, experience



app = FastAPI(root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config('ALLOWED_ORIGINS', cast=lambda v: [
                         s.strip() for s in v.split(',')]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(experience.router, prefix="/experience", tags=["Experience"])