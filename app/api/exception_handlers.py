from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    BonusCalculationBaseError
)


async def bonus_exception_handler(request: Request, exc: BonusCalculationBaseError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )