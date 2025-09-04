from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError
import traceback

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.detail}  # ✅ Теперь всегда {"error": "..."}
            )
        except ValidationError as exc:
            return JSONResponse(
                status_code=422,
                content={"error": exc.errors()[0]['msg']}  # ✅ Берем первое сообщение об ошибке
            )
        except Exception as e:
            print(f"Unhandled exception: {traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error"}
            )

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": exc.errors()[0]['msg']}  # ✅ Выводим только текст ошибки
        )

    @app.exception_handler(Exception)
    async def custom_generic_exception_handler(request: Request, exc: Exception):
        print(f"Unhandled exception: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error"},
        )
