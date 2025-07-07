from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
from models import model_user
from api.schemas import schema_user
from repository import repository_user
from services import service_auth
from utils import security


router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with the provided credentials.",
    response_description="User registration confirmation",
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {"detail": "User successfully registered"}
                }
            }
        },
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email or username already exists"}
                }
            }
        }
    }
)
async def register(
    user: schema_user.UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Register a new user in the system.

    Parameters:
    - **user**: UserCreate schema containing:
        - username (str): Unique username (required)
        - email (str): Valid email address (required)
        - password (str): Strong password (required)
        - full_name (str, optional): User's full name

    Returns:
    - HTTP 201: Successful registration with confirmation message

    Raises:
    - HTTP 409: If username or email already exists
    """
    existing_user_result = await db.execute(
        select(model_user.User).where(
            or_(
                model_user.User.email == user.email,
                model_user.User.username == user.username
            )
        )
    )
    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists"
        )

    user_response = await repository_user.create_user(db, user)

    return JSONResponse(
        content={
            "detail": "User successfully registered",
            "user_uuid": str(user_response.uuid)
        },
        status_code=status.HTTP_201_CREATED
    )

@router.post(
    "/login",
    response_model=schema_user.LoginResponse,
    summary="User login",
    description="Authenticates user credentials and returns an access token.",
    response_description="Login response with access token",
    responses={
        200: {
            "description": "Successful login",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Login successful"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {"detail": "User Not Found or Inactive"}
                }
            }
        },
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid Credentials"}
                }
            }
        }
    }
)
async def login(
    user_credentials: schema_user.LoginRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Authenticate user and generate access token.

    Parameters:
    - **user_credentials**: LoginRequest schema containing:
        - email (str): Registered email address
        - password (str): User's password
        - remember (bool): Whether to create a long-lived token

    Returns:
    - JSONResponse: Sets HTTP-only cookie with access_token and returns success message
        - access_token: JWT token for authenticated requests
        - expires: Token expiration timestamp

    Raises:
    - HTTP 401: If user not found or inactive
    - HTTP 403: If invalid credentials provided
    """
    user_result = await db.execute(
        select(model_user.User).where(
            model_user.User.email == user_credentials.email,
            model_user.User.active == True
        )
    )
    
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found or Inactive"
        )
        

    if not security.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    token_data = service_auth.create_access_token(
        user_uuid=str(user.uuid),
        remember=user_credentials.remember
    )
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

@router.get(
    "/profile",
    response_model=schema_user.UserProfile,
    summary="Get current user",
    description="Returns the authenticated user's information.",
    response_description="User object",
)
async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    access_token: str | None = Cookie(default=None)
):
    return await service_auth.get_user_by_token(db, access_token)
