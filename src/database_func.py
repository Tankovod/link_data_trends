from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from datetime import datetime
from src.database.models import Object, PingTrend, CurrDatetime


def pg_insert_objects(data):
    with Object.session() as session:
        for ob in data:
            try:
                obj = Object(name=ob[0], ip_address=ob[1])
                session.add(obj)
                session.commit()
                session.refresh(obj)
            except IntegrityError:
                pass
            except PendingRollbackError:
                session.rollback()
                try:
                    session.add(obj)
                    session.commit()
                    session.refresh(obj)
                except IntegrityError:
                    pass


def pg_insert_curr_datetime():
    with CurrDatetime.session() as session:
        obj = CurrDatetime(dt=datetime.now())
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj.id


def pg_insert_trends(data, curr_datetime_id: int):
    with PingTrend.session() as session:
        for obj in data:
            p = PingTrend(datetime_id=curr_datetime_id, ping=obj[2])
            p.object_id = session.scalar(select(Object.id).filter(Object.name == obj[0]))
            session.add(p)
            session.commit()
            session.refresh(p)


def pg_select_trends(from_time: datetime, to_time: datetime, object_trend_names: list[str] = None):
    with PingTrend.session() as session:
        if not object_trend_names:
            return session.query(PingTrend.ping, Object.name, CurrDatetime.dt) \
                .join(Object, Object.id == PingTrend.object_id) \
                .join(CurrDatetime, CurrDatetime.id == PingTrend.datetime_id) \
                .filter(CurrDatetime.dt < to_time)\
                .filter(CurrDatetime.dt >= from_time).all()
        return session.query(PingTrend.ping, Object.name, CurrDatetime.dt)\
            .join(Object, Object.id == PingTrend.object_id) \
            .join(CurrDatetime, CurrDatetime.id == PingTrend.datetime_id) \
            .filter(CurrDatetime.dt < to_time) \
            .filter(CurrDatetime.dt >= from_time) \
            .filter(Object.name.in_(object_trend_names)) \
            .all()


objects = [
    ('localhost', '127.0.0.1', False),
    ('localhost1', '127.0.0.1', False),
]


