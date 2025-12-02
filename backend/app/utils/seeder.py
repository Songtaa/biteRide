from typing import Annotated
from app.domains.public.schemas.user_schema import UserCreate
from app.domains.public.services.user_service import UserService
from app.domains.public.models.user import User
from app.domains.tenants.models.tenant_user import TenantUser

from app.domains.public.services.tenant_user_service import TenantUserService
from app.domains.tenants.schemas.tenant_user import TenantUserCreate
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlmodel import SQLModel
from app.utils.dependencies import get_master_session_dep, get_tenant_session_dep
from fastapi import Depends



logger = logging.getLogger(__name__)


sessionDep = Annotated[AsyncSession, Depends(get_master_session_dep)]

tenant_sessionDep = Annotated[AsyncSession, Depends(get_tenant_session_dep)]



async def seed_global_admin_user(
        session: AsyncSession, 
        user_data: UserCreate,
        ) -> None:
    user_service = UserService(
        session)

    if await user_service.user_exists(user_data.email):
        logger.info(f"Global admin user {user_data.email} already exists. Skipping.")
        return

    logger.info(f"Seeding global admin user: {user_data.email}")
    await user_service.create(user_data)
    await session.commit()
    logger.info("Global admin user created successfully.")



async def seed_tenant_admin_user(
    session: AsyncSession, 
    tenant_user_data: TenantUserCreate, 
    user_model: type[TenantUser],
)-> None:
    tenant_user_service = TenantUserService(session, model=user_model)

    if await tenant_user_service.user_exists(tenant_user_data.email):
        logger.info(f"Tenant admin user {tenant_user_data.email} already exists in schema. Skipping.")
        return

    logger.info(f"Seeding tenant admin user in : {tenant_user_data.email}")
    await tenant_user_service.create(tenant_user_data)
    await session.commit()
    logger.info(f"Tenant admin user created successfully in.")



# async def seed_tenant_admin_user(
#     session: AsyncSession, 
#     tenant_user_data: TenantUserCreate, 
#     user_model: type[TenantUser],
# ):
#     service = TenantUserService(session, model=user_model)

#     if await service.user_exists(tenant_user_data.email):
#         logger.info(f"Tenant admin {tenant_user_data.email} already exists. Skipping.")
#         return

#     logger.info(f"Creating tenant admin user: {tenant_user_data.email}")
#     await service.create(tenant_user_data)
#     await session.commit()
#     logger.info("Tenant admin created successfully.")

