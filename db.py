from typing import Optional, Sequence
from datetime import date
import os
from getpass import getuser

from sqlalchemy import Engine, asc, create_engine, delete, func, select, desc
from sqlalchemy.orm import Session, joinedload, sessionmaker

from models import Base, Review, TimeInterval, Topic

class MetaDB(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=MetaDB):
    _engine: Engine
    _Session: sessionmaker[Session]
    _debug: bool

    def __init__(self, debug: bool):
        self._debug = debug
        self._engine = create_engine(
            self._get_absolute_path(),
            echo=True if self._debug else False
        )
        self._Session = sessionmaker(self._engine)

        Base.metadata.create_all(self._engine)

    def _get_absolute_path(self):
        sqlite_dialect_driver = "sqlite+pysqlite://"
        db_file_name = "reviews.db"
        if self._debug:
            return f"{sqlite_dialect_driver}/{db_file_name}"
        
        absolute_path = f"/home/{getuser()}/.local/share/review_planner"
        try:
            os.mkdir(absolute_path)
        finally:
            return f"{sqlite_dialect_driver}/{absolute_path}/{db_file_name}"

    def update_last_review_topic_id(
        self,
        topic_id: int
    ) -> Optional[Review]:
        with self._Session() as session:
            review = session.execute(
                select(Review)
                .where(Review.topic_id == topic_id)
                .options(joinedload(Review.time_interval))
                .order_by(desc(Review.id))
            ).scalar()

            if not review:
                return None

            review.completed = True
            session.commit()
            session.refresh(review)
            return review

    def update_topic(
        self,
        topic_id: int,
        review_at: date,
        interval_id: int
    ) -> Review:
        with self._Session() as session:
            review = Review(
                completed=False,
                review_at=review_at,
                interval_id=interval_id,
                topic_id=topic_id
            )
            session.add(review)
            session.commit()
            session.refresh(review)
            return review

    def delete_topic(self, topic_id: int) -> Optional[Topic]:
        with self._Session.begin() as session:
            topic = session.get(Topic, topic_id)

            if not topic:
                return None

            session.delete(topic)
            return topic

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        with self._Session() as session:
            return session.execute(
                select(Topic)
                .where(Topic.id == topic_id)
                .options(
                    joinedload(Topic.reviews)
                    .joinedload(Review.time_interval)
                )            
            ).scalar()

    def list_topics(self) -> Sequence[Topic]:
        with self._Session() as session:
            return session.execute(
                select(Topic).order_by(Topic.name)
            ).scalars().fetchall()

    def get_topic_by_name(self, topic_name: str) -> Optional[Topic]:
        with self._Session() as session:
            return session.execute(
                select(Topic)
                .where(Topic.name == topic_name)
            ).scalar()

    def get_time_interval_by_id(
        self,
        interval_id: int
    ) -> TimeInterval:
        with self._Session() as session:
            return session.execute(
                select(TimeInterval)
                .where(TimeInterval.id == interval_id)
            ).scalar_one()

    def get_ord_asc_intervals(self) -> Sequence[TimeInterval]:
        with self._Session() as session:
            return session.execute(
                select(TimeInterval)
                .order_by(asc(TimeInterval.interval))
            ).scalars().fetchall()

    def count_time_intervals(self) -> int:
        with self._Session() as session:
            return session.execute(
                select(func.count())
                .select_from(TimeInterval)
            ).scalar_one()

    def add_topic(
        self,
        topic_name: str,
        interval: TimeInterval
    ) -> tuple[Topic, Review]:
        with self._Session() as session:
            session.expire_on_commit = False
            topic = Topic(name=topic_name)

            review = Review(
                completed=False,
                review_at=date.fromordinal(
                    date.toordinal(date.today()) + interval.interval
                ),
                time_interval=interval,
                topic=topic
            )

            topic.reviews.append(review)
            session.add_all([topic, review])
            session.commit()

            session.refresh(topic)
            session.refresh(review)
            return (topic, review)
    
    def _init_time_intervals(self):
        with self._Session.begin() as session:
            required_intervals = [
                TimeInterval(id=1, interval=1, name="d+1"),
                TimeInterval(id=2, interval=7, name="d+7"),
                TimeInterval(id=3, interval=30, name="d+30"),
                TimeInterval(id=4, interval=14, name="d+14"),
            ]

            intervals = session.execute(
                select(TimeInterval)
            ).fetchall()

            if len(intervals) != len(required_intervals):
                session.execute(
                    delete(TimeInterval)
                )
                session.add_all(required_intervals)

