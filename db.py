from typing import Optional, Sequence
from datetime import date

from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session, joinedload

from models import Base, Review, TimeInterval, Topic

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
            echo=False
        )

        Base.metadata.create_all(self.engine)
        pass

    def update_topic(self, topic_id: int) -> Optional[Review]:
        with Session(self.engine) as session:
            reviews = session.execute(
                select(Review)
                .where(Review.topic_id == topic_id)
                .order_by(desc(Review.id))
            ).scalars().fetchall()

            if not reviews:
                return None

            last_review = reviews[0]

            if not last_review.interval_id == 3:
                return None

            next_interval = session.execute(
                select(TimeInterval)
                .where(TimeInterval.id == last_review.interval_id + 1)
            ).scalar()

            if not next_interval:
                print("Database not initialized.")
                return None

            review = Review(
                completed=False,
                review_at=date.fromordinal(
                    date.toordinal(date.today()) + next_interval.interval
                ),
                time_interval=next_interval,
                topic_id=topic_id
            )
            last_review.completed = True
            session.add(review)
            session.commit()
            return review

    def delete_topic(self, topic_id: int) -> Optional[Topic]:
        with Session(self.engine) as session:
            topic = session.get(Topic, topic_id)

            if not topic:
                return None

            session.delete(topic)
            session.commit()
            return topic

    def get_topic(self, topic_id: int) -> Optional[Topic]:
        with Session(self.engine) as session:
            return session.execute(
                select(Topic)
                .where(Topic.id == topic_id)
                .options(
                    joinedload(Topic.reviews)
                    .joinedload(Review.time_interval)
                )            
            ).scalar()

    def list_topics(self) -> Sequence[Topic]:
        with Session(self.engine) as session:
            return session.execute(
                select(Topic).order_by(Topic.name)
            ).scalars().fetchall()

    def add_topic(self, topic_name: str) -> Optional[int]:
        with Session(self.engine) as session:
            topic = session.execute(
                select(Topic)
                .where(Topic.name == topic_name)
            ).one_or_none()

            if topic:
                return None

            topic = Topic(name=topic_name)
            interval = session.get(TimeInterval, 1)

            if not interval:
                print("Database not initialized")
                return None

            review = Review(
                completed=False,
                review_at=date.fromordinal(
                    date.toordinal(date.today()) + interval.interval
                ),
                time_interval=interval,
                topic=topic
            )

            topic.reviews.append(review)
            session.add(topic)
            session.add(review)
            session.commit()
            return topic.id
    
    def _init_time_intervals(self):
        with Session(self.engine) as session:
            intervals = session.execute(
                select(TimeInterval)
            ).fetchall()

            if len(intervals) == 0:
                session.add(TimeInterval(id=1, interval=1, name="d+1"))
                session.add(TimeInterval(id=2, interval=7, name="d+7"))
                session.add(TimeInterval(id=3, interval=30, name="d+30"))
                session.commit()
