from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from ..db.main import get_db
from .utils import create_access_token, hash_password, verify_password
from ..schemas import LoginRequest, RegisterRequest,TokenResponse
from ..db.models import User


user_router = APIRouter()


@user_router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):

    # Check whether username already exists
    existing_user = (
        db.query(User)
        .filter(
            User.username == data.username
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )


    # Hash password
    hashed_password = hash_password(
        data.password
    )


    # Create user
    user = User(
        username=data.username,
        password_hash=hashed_password,
        scopes="user",
        textbee_device_id=data.textbee_device_id,
        textbee_api_key=data.textbee_api_key,
    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return {
        "message": "User created successfully",
        "user_id": user.id,
        "username": user.username,
    }



@user_router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    # Find user
    user = (
        db.query(User)
        .filter(
            User.username == data.username
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )


    # Verify password
    if not verify_password(
        data.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )


    # Convert scopes from DB string to list
    scopes = user.scopes.split()
    print(f"User scopes: {scopes}")


    # Create JWT
    token = create_access_token(
        user_id=user.id,
        username=user.username,
        scopes=scopes,
    )


    return {
        "access_token": token,
        "token_type": "bearer",
    }