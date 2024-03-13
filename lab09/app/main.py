from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='username already registered')
    return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get('/users/{username}', response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@app.get('/users/{username}/verify/', response_model=schemas.UserDetail)
def verify_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User authentication failed')
    return db_user

@app.get('/users/{username}/pastes/', response_model=List[schemas.Paste])
def get_user_pastes(username: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    pastes = crud.get_user_pastes(db, db_user.id, skip=skip, limit=limit)
    return pastes

# @app.post('/users/{username}/pastes/', response_model=schemas.PasteCreate)
# def create_paste(username: str, password: str, paste:schemas.PasteBase, db: Session = Depends(get_db)):
#     db_user = crud.verify_user(db, username=username, password=password)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User authentication failed')
#     created_paste = crud.create_paste(db=db, paste=paste, owner=db_user)
#     return created_paste

@app.post('/users/{username}/create_paste', response_model=schemas.Paste)
def create_paste(username: str, password: str, paste: schemas.PasteBase, db:Session = Depends(get_db)):
    db_user = crud.verify_user(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User authentication failed')
    
    return crud.create_paste(db=db, paste=paste, owner_id=db_user.id)

@app.get('/pastes/', response_model=List[schemas.PasteBase])
def get_pastes_length(db: Session = Depends(get_db)):
    paste_length = crud.get_pastes_length(db)
    return paste_length