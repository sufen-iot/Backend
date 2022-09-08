from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = f"mysql+mysqlconnector://noahdy:pa$$w0rd@plebea.site:3306/"
DATABASE_URL = f"mysql+mysqlconnector://root:1234@localhost:3306/sufen?charset=utf8"
engine = create_engine(DATABASE_URL, encoding="utf-8")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

