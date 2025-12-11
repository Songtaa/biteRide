from fastapi import APIRouter, Depends
from app.domains.public.apis.login_router import auth_router
from app.domains.public.apis.tenant import tenant_management_router
from app.domains.public.apis.users_router import user_router
from app.domains.public.apis.role import role_router
from app.domains.public.apis.permission import permission_router
from app.domains.public.apis.rider import rider_router
from app.domains.public.apis.rider_tenants import rider_tenant_router
from app.domains.public.apis.tenant_riders import tenant_rider_router
from app.domains.public.apis.payment_gateway import payment_router

from app.config.tenant_dependencies import require_global_context

global_router = APIRouter(dependencies=[Depends(require_global_context)])
global_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
global_router.include_router(tenant_management_router, prefix="/tenants", tags=["Tenants management"])
global_router.include_router(user_router, prefix="/users", tags=["Users"])
global_router.include_router(role_router, prefix="/roles", tags=["Roles"])
global_router.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
global_router.include_router(rider_router, prefix="/riders", tags=["Riders"])
global_router.include_router(rider_tenant_router, prefix="/riders", tags=["Rider Tenants"])
global_router.include_router(tenant_rider_router, prefix="/riders", tags=["Tenant Riders"])
global_router.include_router(payment_router, prefix="/payment-gateways", tags=["Payment Gateways"])
