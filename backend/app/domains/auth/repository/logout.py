from crud.base import CRUDBase
from domains.auth.models.user import User
from domains.auth.schemas.user_account import (
    UserCreate, UserUpdate
)


class CRUDLoggedOutUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass
logged_out_users_actions = CRUDLoggedOutUser(User)