from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_database():
    Base.metadata.create_all(bind=engine)

def getSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

if __name__ == '__main__':
    create_database()