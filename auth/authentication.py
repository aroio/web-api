from datetime import datetime, timedelta
from hashlib import sha512

import jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pydantic import BaseModel

class Authentication:

    @staticmethod
    def authenticate(
        aroio_name: str,
        aroio_password: str,
        username: str,
        password: str) -> bool:
        """Authentication specified to Aroio with the username and password"""
        if username != aroio_name:
            return False
        if not self.verify_password(plain=password,hashed=aroiopassword):
            return False
        return True


    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verification of password input"""
        return self.hash_password(plain) == hashed


    @staticmethod
    def hash_password(password: str) -> str:
        """Creates hash of password"""
        return sha512(str(password).encode("utf-8")).hexdigest()
