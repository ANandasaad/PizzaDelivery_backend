
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from Schemas.auth import TokenData

pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def hashPassword(password: str):
    return pwd_cxt.hash(password)

def verifyPassword(password: str, hashedPassword: str):
    return pwd_cxt.verify(password, hashedPassword)

def createToken(data: dict):

    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token:str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("email")
        id= payload.get("id")
        role= payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role, id=id)
        # return user id and username
        return token_data

    except InvalidTokenError:
        raise credentials_exception


