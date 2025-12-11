# app/config/tenant_dependencies.py
from app.domains.public.models.tenant import Tenant
from fastapi import Request, HTTPException, Depends
from typing import Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_tenant_session, get_master_session
from app.domains.public.services.tenant import TenantService
from app.domains.public.repository.tenant import TenantRepository
from sqlmodel import Session, select


from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_tenant_id_from_context(request: Request) -> str:
    """
    Uses tenant_id set by TenantSubdomainMiddleware.
    """
    tenant_id = getattr(request.state, "tenant_id", None)
    context = getattr(request.state, "context", None)

    if context != "tenant" or not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant context required")

    return tenant_id


def get_tenant_session_from_context(request: Request) -> AsyncSession:
    """
    Returns the tenant session injected by TenantSubdomainMiddleware.
    """
    session = getattr(request.state, "session", None)
    context = getattr(request.state, "context", None)

    if context != "tenant" or session is None:
        raise HTTPException(status_code=400, detail="Tenant session unavailable")

    return session


def require_global_context(request: Request):
    if getattr(request.state, "context", None) != "global":
        raise HTTPException(status_code=403, detail="Global context required")


def require_tenant_context(request: Request):
    if getattr(request.state, "context", None) != "tenant":
        raise HTTPException(status_code=403, detail="Tenant context required")

# async def get_tenant_id(request: Request) -> UUID:
#     """Resolve tenant UUID from subdomain or header with proper database lookup"""
#     tenant_identifier = None
    
    
#     host = request.headers.get("host", "").split(".")
#     if len(host) > 2 and host[0] != "www":
#         tenant_identifier = host[0]
    
#     if not tenant_identifier:
#         tenant_identifier = request.headers.get("X-Tenant-ID")
    
#     if not tenant_identifier:
#         raise HTTPException(status_code=400, detail="Tenant not specified")

    
#     async with get_master_session() as session:
#         tenant_repo = TenantRepository(session)

#         try:
            
#             try:
#                 tenant_uuid = UUID(tenant_identifier)
#                 tenant = await tenant_repo.get(Tenant, tenant_uuid)
#                 if tenant:
#                     return tenant.id
#             except ValueError:
#                 pass  
            
#             stmt = select(Tenant).where(Tenant.subdomain == tenant_identifier)
#             result = await session.execute(stmt)
#             tenant = result.scalars().first()
            
#             if tenant:
#                 return tenant.id
            
#             raise HTTPException(status_code=404, detail="Tenant not found")
            
#         except Exception as e:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Failed to resolve tenant: {str(e)}"
#             )

# async def get_tenant_session(tenant_id: UUID = Depends(get_tenant_id)) -> AsyncSession:
#     """Get tenant-specific database session using resolved UUID"""
#     try:
#         async with get_tenant_session(str(tenant_id)) as session:
#             yield session
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to establish tenant session: {str(e)}"
#         )

# def require_global_context(request: Request):
#     if getattr(request.state, "context", None) != "global":
#         raise HTTPException(status_code=403, detail="Only accessible from global context")


# def require_tenant_context(request: Request):
#     if getattr(request.state, "context", None) != "tenant":
#         raise HTTPException(status_code=403, detail="Only accessible from tenant context")

