
# from app.domains.school.models.tenant_role import TenantUserRole

from app.domains.auth.models.refresh_token import RefreshToken
from app.domains.auth.models.token_blocklist import TokenBlocklist

from app.domains.tenants.models.tenant import Tenant
from app.domains.auth.models.rbac_models import (
    User, 
    Role, 
    Permission, 
    UserRole, 
    RolePermission, 
    UserPermission,
)

from app.domains.tenants.models.tenant_rbac_models import (
    TenantUser,
    TenantRole,
    TenantUserRole,
    TenantUserPermission,
    TenantRolePermission,
    TenantPermission,
)
