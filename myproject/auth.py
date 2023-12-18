from passlib.context import CryptContext
import crud
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


# Hash the password at user creation
def get_password_hash(password):
    return pwd_context.hash(password)


# Verify the hashed password with the plaintext password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Make a login/authentication system
def authenticate_player(db: Session, username: str, password: str):
    player = crud.get_player_by_username(db, username)
    if not player:
        return False
    if not verify_password(password, player.password_hash):
        return False
    return player


SECRET_KEY = "2276616bf52d426247af8796a80e2b2877b362760fee2fa9dc073b62e57845d1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create the access token for the site using the SSL-key
def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes of expiration time
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Adding the JWT expiration time case
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
