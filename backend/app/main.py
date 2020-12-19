from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from app import services
from app.api.api_v1.api import api_router
from app.core.config import settings

from app.db.session import SessionLocal

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
@repeat_every(seconds=60)  # 1 minute
def cancel_missed_reservations_task() -> None:
    db = SessionLocal()
    services.reservation.cancel_missed_reservations(db)
    db.close()
