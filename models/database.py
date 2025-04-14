import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

engine = db.create_engine(settings.DATABASE_URL)
session = sessionmaker(bind=engine)()

Base = declarative_base()

class VesselDB(Base):
    __tablename__ = "vessels"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

Base.metadata.create_all(engine)