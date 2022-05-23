from datetime import datetime
from email.policy import default
from sqlalchemy import Boolean, Integer, String, DateTime, Time, ForeignKey, Column
from sqlalchemy.orm import relationship, declarative_base 
from sqlalchemy.sql import func

Base = declarative_base()

# Create your models here.

class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    hid = Column(String, default='')
    name = Column(String, default='')
    age = Column(Integer, default=0)
    gender = Column(String, default='')
    weight = Column(Integer, default=0)
    height = Column(Integer, default=0)
    notes = Column(String)
    datetime = Column(DateTime, default=func.now())
    recent = Column(DateTime, default=func.now(), onupdate=func.now())
    pe = Column(Boolean, default=False)


    scan = relationship('Scan', back_populates='patient', uselist=False)


class Scan(Base):
    __tablename__ = "scan"
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('patient.id'), nullable=True)
    pname = Column(String, default='')

    name = Column(Integer, default=0)
    data = Column(String, default='')
    v3d = Column(String, default='')

    datetime = Column(DateTime, default=func.now())

    patient = relationship('Patient', foreign_keys=[pid])


class Settings(Base):
    __tablename__= "settings"
    id = Column(Integer, primary_key=True)
    localizer = Column(Boolean, default=False)
    pdf = Column(Boolean, default=True)
    csv = Column(Boolean, default=True)
    pic_format = Column(String, default='png')
    v3d = Column(Boolean, default=False)
    results = Column(String, default='binary')
