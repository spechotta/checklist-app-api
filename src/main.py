from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.checklists import models
from src.checklists.controller import router as checklist_router
from src.database import engine

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

#CORS Middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Register checklist routes with the main FastAPI application
app.include_router(checklist_router)