import os
import sys
from sqlalchemy import Column, Integer, String, Text, Float,BigInteger

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
from db_setup import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    distance = Column(Float, nullable=True)
    average_speed = Column(Float, nullable=True)
    average_heartrate = Column(Float, nullable=True)
