from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"}
    )

def register_user_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)