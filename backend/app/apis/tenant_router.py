from fastapi import APIRouter, Depends
from app.config.tenant_dependencies import require_tenant_context
from app.domains.tenants.apis.vendor import vendor_router
from app.domains.tenants.apis.category import category_router

tenant_router = APIRouter(dependencies=[Depends(require_tenant_context)])
tenant_router.include_router(vendor_router, prefix="/vendors", tags=["Vendors"])
tenant_router.include_router(category_router, prefix="/categories", tags=["Categories"])

