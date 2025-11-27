from typing import List, Optional

from app.crud.base import BaseRepository, ModelType
# from app.domains.auth.models.rbac_models import User
# from app.domains.auth.models.rbac_models import UserRole
from app.domains.auth.models.user import User
from app.domains.auth.models.user_role import UserRole
from app.domains.auth.schemas.user_schema import UserCreate, UserSchema, UserUpdate
from pydantic import UUID4
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from app.utils.security import Security
from uuid import UUID
from typing import List, Type
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload


class CRUDUser(BaseRepository[User, UserCreate, UserUpdate]):
    pass

async def some_function(session: AsyncSession):
    users_form_actions = CRUDUser(User, session)
# users_form_actions = CRUDUser(User)


class UserRepository(BaseRepository[ModelType, UserCreate, UserUpdate]):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        super().__init__(model, session)


    async def get_all(self) -> List[Optional[UserSchema]]:
        statement = select(User)
        result = await self.session.execute(statement)
        users = result.scalars().all()
        return [UserSchema(**user.__dict__) for user in users]


    async def get_user_by_email(self, email: str):
        # statement = select(User).where(User.email == email)
        statement = select(User).options(selectinload(User.user_roles)).where(User.email == email)

        result = await self.session.execute(statement)

        user = result.scalar()

        return user

    async def get_user_by_id(self, user_id: UUID):
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement) 
        user = result.scalars().first()
        return user

    

    async def create_user(self, user_data: UserCreate):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password = Security.generate_password_hash(user_data_dict["password"])
        # new_user.role = "user"


        self.session.add(new_user)

        await self.session.commit()

        return new_user

    async def update(self, user: Type[User], user_data: UserUpdate)-> UserSchema:
        try:
            
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)

            
            await self.session.commit()
            await self.session.refresh(user)  
            return UserSchema(**user.__dict__)
        except NoResultFound:
            return None  
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_user(self, user:Type[User]):
        try:

            await self.session.delete(user)
            await self.session.commit()
            return True
        except NoResultFound:
            return None
        except Exception as e:
            await self.session.rollback()
            raise e


    def assign_role(self, user_id: UUID, role_id: UUID):
        user_roles = UserRole(user_id=user_id, role_id=role_id)
        self.session.add(user_roles)
        self.session.commit()
        return {"message": "Role assigned successfully"}
    
    
# user_repository = UserRepository()