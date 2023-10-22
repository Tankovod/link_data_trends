from sqlalchemy import VARCHAR, TIMESTAMP, ForeignKey, BOOLEAN, INT, BIGINT
from sqlalchemy.orm import relationship
from src.database.database import Base, Column


class PingTrend(Base):
    __tablename__ = 'ping_trend'
    datetime_id = Column(BIGINT, ForeignKey('curr_datetime.id', ondelete='CASCADE'), nullable=False)
    object_id = Column(INT, ForeignKey('object.id', ondelete='CASCADE'), nullable=False)
    ping = Column(BOOLEAN, nullable=False)


class CurrDatetime(Base):
    __tablename__ = 'curr_datetime'
    dt = Column(TIMESTAMP, nullable=False, unique=True)
    trend = relationship('PingTrend', backref='CurrDatetime')


class Object(Base):
    __tablename__ = 'object'
    name = Column(VARCHAR(32), unique=True, nullable=False)
    ip_address = Column(VARCHAR(32), unique=False, nullable=False)
    trend = relationship('PingTrend', backref='Object')





