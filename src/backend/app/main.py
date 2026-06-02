from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import clients_router, policies_router, summary_router
from app.db.session import Base, engine
from app.models import Advisor, Client, ManagementAction, Policy


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Insurance Portfolio API",
    description="API para gestionar cartera de pólizas, renovaciones y acciones comerciales.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(clients_router)
app.include_router(policies_router)
app.include_router(summary_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
