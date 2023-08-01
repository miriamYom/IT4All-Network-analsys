from fastapi import Response, Depends, Body, HTTPException, status, encoders, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import Json
from auth.auth_handler import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    add_user
from auth.auth_models import Token
from models.entities import UserInDB, UserLogin

router = APIRouter()


@router.post("/sign_up")
async def sign_up(user: UserLogin = Body(...)):
    try:
        user_id = await add_user(user)
    except Exception as e:
        # TODO: error logging
        raise HTTPException(status_code=500, detail=e)
    return f"user added with id:{user_id}"


@router.post("/login", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # TODO: add username in data
    access_token = create_access_token(
        data={"email": user.Email, "first_name": user.FirstName, "last_name": user.LastName},
        expires_delta=access_token_expires

    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}
