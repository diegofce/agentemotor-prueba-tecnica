from app.api.routes.clients import router as clients_router
from app.api.routes.policies import router as policies_router
from app.api.routes.summary import router as summary_router

__all__ = ["clients_router", "policies_router", "summary_router"]
