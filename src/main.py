from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.checklists import checklist_models
from src.checklists.checklist_controller import router as checklist_router
from src.checklists.checklist_exceptions import register_checklist_exception_handlers
from src.database import engine
from src.users import user_models
from src.users.user_controller import router as user_router
from src.users.user_exceptions import register_user_exception_handlers

app = FastAPI()

# Create tables for checklists and users modules
checklist_models.Base.metadata.create_all(bind = engine)
user_models.Base.metadata.create_all(bind = engine)

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

# Register checklist and user routes with the FastAPI app
app.include_router(checklist_router)
app.include_router(user_router)

# Register exception handlers with the FastAPI app
register_checklist_exception_handlers(app)
register_user_exception_handlers(app)