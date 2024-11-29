from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str):
    return pwd_cxt.hash(password)