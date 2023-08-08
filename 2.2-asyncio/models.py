from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text

PG_DSN = 'postgresql+asyncpg://postgres:1@127.0.0.1:5432/swapi_db'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class SwapiPeople(Base):
    __tablename__ = 'swapi_people'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    birth_year = Column(Text)
    eye_color = Column(Text)
    films = Column(Text)
    gender = Column(Text)
    hair_color = Column(Text)
    height = Column(Text)
    homeworld = Column(Text)
    mass = Column(Text)
    name = Column(Text)
    skin_color = Column(Text)
    species = Column(Text)
    starships = Column(Text)
    vehicles = Column(Text)