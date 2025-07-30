from fastapi import FastAPI

from routers.user_routes import user_router
from routers.tenant_routes import tenant_router
from routers.activity_routes import activity_router
from routers.project_routes import project_router

app = FastAPI()
app.include_router(user_router, prefix="/auth", tags=["Users"])
app.include_router(tenant_router, prefix='/api')
app.include_router(activity_router, prefix='/api')
app.include_router(project_router, prefix='/api')

