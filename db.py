from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, TimeInterval

class MetaDB(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=MetaDB):
    def __init__(self):
        self.engine = create_engine(
            "sqlite+pysqlite:///reviews.db",
            echo=True
        )

        Base.metadata.create_all(self.engine)
        pass
    
    def _init_time_intervals(self):
        with Session(self.engine) as session:
            intervals = session.execute(
                select(TimeInterval)
            ).fetchall()

            if len(intervals) == 0:
                session.add(TimeInterval(id=1, interval="d+1"))
                session.add(TimeInterval(id=2, interval="d+7"))
                session.add(TimeInterval(id=3, interval="d+30"))
                session.commit()
