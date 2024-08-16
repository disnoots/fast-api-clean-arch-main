import http

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.domains.auth.auth_http import router as auth_router
from src.domains.book.book_http import router as book_router

app = FastAPI(title="OBP RBP Backend")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content=jsonable_encoder(
            {
                "error": " ".join([str(i) for i in exc.errors()[0]['loc']]) + " " + exc.errors()[0]["msg"],
                "status_code": http.HTTPStatus.BAD_REQUEST,
            }
        ),
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    err = " ".join([str(i) for i in exc.errors()[0]['loc']])
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content=jsonable_encoder(
            {
                "error": err + ": " + exc.errors()[0]["msg"],
                "status_code": http.HTTPStatus.BAD_REQUEST,
            }
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": exc.detail, "status_code": exc.status_code}),
    )


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status_code": 500, "error": str(exc)}),
    )


app.include_router(auth_router)
app.include_router(book_router)
