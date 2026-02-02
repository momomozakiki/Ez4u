# import pytest
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt

def test_password_hashing():
    password = "secret"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_creation():
    username = "testuser"
    token = create_access_token(subject=username)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == username
    assert "exp" in payload

def test_jwt_expiration():
    username = "testuser"
    # Create token expiring in future
    token = create_access_token(subject=username, expires_delta=timedelta(minutes=1))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == username
