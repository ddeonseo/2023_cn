from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mariadb+mariadbconnector://pasteuser:user-secret-pw@127.0.0.1:3306/pastebin'
#pasteuser:user-secret-pw: DB에 연결할 사용자 이름과 암호 제공

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# bind: 세션이 사용할 데이터베이스 엔진을 지정
Base = declarative_base()