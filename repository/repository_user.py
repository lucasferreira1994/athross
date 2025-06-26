from sqlalchemy.ext.asyncio import AsyncSession
from models import model_user
from api.schemas import schema_user
from utils import security

async def create_user(db: AsyncSession, user: schema_user.UserCreate) -> model_user.User:
    security.validate_password(user.password, user.confirm_password)
    encrypted_password = security.hash_password(user.password)
    user = model_user.User(
        username=user.username,
        email=user.email, 
        password=encrypted_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_profile(
    db: AsyncSession,
    user: model_user.User,
    username: str,
    email: str,
    password: str | None,
    confirm_password: str | None,
) -> model_user.User:
    user.username = username
    user.email = email

    if password and password.strip():
        security.validate_password(password, confirm_password)
        user.password_hash = security.hash_password(password)

    await db.commit()
    await db.refresh(user)

    return user


async def get_user(db: AsyncSession, user_uuid: str) -> model_user.User:
    return await db.get(model_user.User, user_uuid)