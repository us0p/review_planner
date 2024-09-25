from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship

from datetime import date


class Base(DeclarativeBase):
    pass


class Topic(Base):
    __tablename__ = "topic"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    reviews: Mapped[List["Review"]] = relationship(
        back_populates="topic", cascade="delete,delete-orphan"
    )


class TimeInterval(Base):
    __tablename__ = "time_interval"

    id: Mapped[int] = mapped_column(primary_key=True)
    interval: Mapped[int] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    reviews: Mapped[List["Review"]] = relationship(
        back_populates="time_interval"
    )


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(
        ForeignKey(Topic.id), nullable=False
    )
    interval_id: Mapped[int] = mapped_column(
        ForeignKey(TimeInterval.id), nullable=False
    )
    review_at: Mapped[date] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)

    time_interval: Mapped[TimeInterval] = relationship(
        back_populates="reviews"
    )
    topic: Mapped[Topic] = relationship(back_populates="reviews")
