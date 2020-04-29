from hashlib import sha512

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
        if not Authentication.verify_password(plain=password,hashed=aroio_password):
            return False
        return True


    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verification of password input"""
        return Authentication.hash_password(plain) == hashed


    @staticmethod
    def hash_password(password: str) -> str:
        """Creates hash of password"""
        return sha512(str(password).encode("utf-8")).hexdigest()
