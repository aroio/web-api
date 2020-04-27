from hashlib import sha512

class Security:
  
  def verify_password(plain: str, hashed: str) -> bool:
    """Verification of password input"""
    return self.hash_password(plain) == hashed

  def hash_password(password: str) -> str:
    """Creates hash of input"""
    return sha512(str(password).encode("utf-8")).hexdigest()