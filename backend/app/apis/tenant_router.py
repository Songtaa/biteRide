from fastapi import APIRouter, Depends
from app.config.tenant_dependencies import require_tenant_context

tenant_router = APIRouter(dependencies=[Depends(require_tenant_context)])
# tenant_router.include_router(user_router, prefix="/users", tags=["Users"])
# tenant_router.include_router(role_router, prefix="/roles", tags=["Roles"])
# tenant_router.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
# tenant_router.include_router(service_router, prefix="/services", tags=["Services"])
