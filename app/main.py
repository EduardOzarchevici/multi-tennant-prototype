from fastapi import FastAPI

from routers.user_routes import user_router
from routers.tenant_routes import tenant_router

app = FastAPI()
app.include_router(user_router, prefix="/auth", tags=["Users"])
app.include_router(tenant_router, prefix='/api')

