import hashlib
import secrets
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).order_by(models.User.id.asc()).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    m = hashlib.sha256()
    salt = secrets.token_bytes(16).hex()
    m.update(user.password.encode('utf-8'))
    m.update(bytes.fromhex(salt))
    password = m.hexdigest()

    db_user = models.User(username=user.username, salt=salt, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def verify_user(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    m.update(bytes.fromhex(db_user.salt))
    password = m.hexdigest()
    if db_user.password != password:
        return None

    return db_user

def create_paste(db: Session, paste: schemas.PasteBase, owner_id: int):
    title = paste.title
    content = paste.content

    db_paste = models.Paste(title=title, content=content, owner_id=owner_id)
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)

    return db_paste

def get_user_pastes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Paste).filter(models.Paste.owner_id == user_id).offset(skip).limit(limit).all()

def get_pastes_length(db: Session):
    return db.query(models.Paste).all()