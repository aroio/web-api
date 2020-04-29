from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from data import datasource
from models import Aroio, Token, TokenData

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET = "81acf31fcffa143203476a6f773aebcb2926c7ccefdcb54c9e4699a950e620e9"


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Creates a JWT with default time delta of 30 minutes"""
    to_encode = data.copy()
    to_encode.update({"exp": expires_delta})
    return jwt.encode(to_encode, key=SECRET, algorithm=ALGORITHM)

# Scheme to be used for the authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/token", response_model=Token, tags=["auth"])
def login_for_access_token(formData: OAuth2PasswordRequestForm=Depends()):
    db_aroio: Aroio = datasource.load_aroio()
    auth_result = Authentication.authenticate(
        aroio_name=db_aroio.name,
        aroio_password=db_aroio.configuration.system.userpasswd,
        username=formData.username,
        password=formData.password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_aroio})
    return {"access_token": access_token, "token_type": "bearer"}


def get_auth_aroio(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username)
    except PyJWTError:
        raise credentials_exception
    aroio = datasource.load_aroio()
    if aroio.name != username:
        raise credentials_exception
    return aroio
