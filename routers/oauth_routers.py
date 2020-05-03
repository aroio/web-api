from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from typing import Union

from data import datasource
from models import Aroio, Token
from auth import Authentication
from exceptions import UnauthorizedException

router = APIRouter()

ACCESS_TOKEN_EXPIRE_DAYS = 1
ALGORITHM = "HS256"
SECRET = "81acf31fcffa143203476a6f773aebcb2926c7ccefdcb54c9e4699a950e620e9"
TOKEN_TYPE = "bearer"

def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)) -> Token:
    """Creates a JWT with default time delta of 30 minutes"""
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, key=SECRET, algorithm=ALGORITHM)
    return Token(token=access_token, token_type=TOKEN_TYPE)


# Scheme to be used for the authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_auth_aroio(token: str = Depends(oauth2_scheme)):
    """Getting an authenticated Aroio"""
    credentials_exception = UnauthorizedException(detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        aroio_dict = payload.get("sub")
        aroio_name = aroio_dict["name"]
        if aroio_name is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    aroio = datasource.load_aroio()
    if aroio.name != aroio_name:
        raise credentials_exception
    return aroio


class LoginForm(BaseModel):
    username: str
    password: str


@router.post("/token", tags=["auth"])
def login_for_access_token(formData: LoginForm):
    """The login route to use in production"""
    db_aroio: Aroio = datasource.load_aroio()
    if db_aroio.authentication_enabled:
        auth_result = Authentication.authenticate(
            aroio_name=db_aroio.name,
            aroio_password=db_aroio.password,
            username=formData.username,
            password=formData.password)
        if not auth_result:
            raise UnauthorizedException(
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

    return create_access_token(data={"sub": db_aroio.dict()})


class AroioSetup(BaseModel):
    verify_password: str
    name: str
    description: str
    authentication_enabled: bool = True


@router.patch("/aroio", tags=["auth"])
def update_aroio_setup(setup: AroioSetup, aroio: Aroio = Depends(get_auth_aroio)):
    """Changing the base Aroio setup with name, password,
    description and authentication_enabled. Returns new access token,
    that must be used for further use of this API. For authentication 
    the current password must be given"""
    authorized = Authentication.verify_password(plain=setup.verify_password, hashed=aroio.password)
    if not authorized:
        raise UnauthorizedException(
            detail="Not authorized changing authorization parameters",
            headers={"WWW-Authenticate": "Bearer"}
        )

    aroio.name = setup.name
    aroio.description = setup.description
    aroio.authentication_enabled = setup.authentication_enabled

    datasource.save(aroio=aroio)

    return create_access_token(data={"sub": aroio.dict()})


class AroioPasswordForm(BaseModel):
    old_password: str
    new_password: str


@router.patch("/aroio/password", tags=["auth"])
async def change_aroio_password(form: AroioPasswordForm, aroio: Aroio = Depends(get_auth_aroio)):
    """`new_password` replaces password for Aroio. `old_password` is required for authentication."""
    auth = Authentication.verify_password(hashed=aroio.password, plain=form.old_password)
    if not auth:
        raise UnauthorizedException(detail="Wrong password")
    
    aroio.password = Authentication.hash_password(password=form.new_password)
    datasource.save(aroio=aroio)
    return create_access_token(data={"sub": aroio.dict()})
