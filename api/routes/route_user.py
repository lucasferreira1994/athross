from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from models import model_user
from api.schemas import schema_user
from services import service_user, service_auth
from utils import security



router = APIRouter(prefix="/user", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: schema_user.UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    user = await db.execute(
        select(model_user.User).where(
            or_(
                model_user.User.email == user.email,
                model_user.User.username == user.username
            )
        )
    )
    user = user.scalar_one_or_none()
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email or username already exists")

    await service_user.create_user(db, user)

    return HTTPException(detail="User successfully registered", status_code=status.HTTP_201_CREATED)

# aplicar access token quando front end estiver pronto
@router.post("/login", response_model=schema_user.LoginResponse)
async def login(user_credentials: schema_user.LoginRequest, db: Session = Depends(get_async_db)):
    user = await db.execute(
        select(model_user.User).where(
            or_(
                model_user.User.email == user.email,
                model_user.User.active == True
            )
        )
    )
    user = user.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found or Inactive")
    
    if not security.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    token_data = service_auth.create_access_token(user_uuid=str(user.uuid), remember=user_credentials.remember)
    access_token = token_data["access_token"]
    max_age = token_data["exp"]

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=max_age,
        expires=max_age,
        samesite="Lax",
        secure=False
    )
    return response
