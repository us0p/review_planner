from db import Database
from tabulate import tabulate

from datetime import date


class Controller:
    def __init__(self, db: Database):
        self.db = db
        self.topic_headers = ["ID", "Name"]
        self.review_headers = [
            "ID",
            "Review at",
            "Interval",
            "Completed",
        ]
        self.list_review_headers = [
            "ID",
            "Topic",
            "Interval",
            "Review at",
            "Completed",
        ]

    def list_reviews_from_completed(self, completed: bool):
        reviews = self.db.get_reviews_from_completed(completed)

        print(
            tabulate(
                [
                    [
                        r.topic.id,
                        r.topic.name,
                        r.time_interval.name,
                        r.review_at,
                        r.completed,
                    ]
                    for r in reviews
                ],
                headers=self.list_review_headers,
            )
        )

    def list_revies(self):
        reviews = self.db.get_reviews()

        print(
            tabulate(
                [
                    [
                        r.topic.id,
                        r.topic.name,
                        r.time_interval.name,
                        r.review_at,
                        r.completed,
                    ]
                    for r in reviews
                ],
                headers=self.list_review_headers,
            )
        )

    def list_reviews_from_date(self, review_at: date):
        reviews = self.db.get_reviews_from_date(date.isoformat(review_at))

        print(
            tabulate(
                [
                    [
                        r.topic.id,
                        r.topic.name,
                        r.time_interval.name,
                        r.review_at,
                        r.completed,
                    ]
                    for r in reviews
                ],
                headers=self.list_review_headers,
            )
        )

    def update(self, topic_id: int):
        last_review = self.db.update_last_review_topic_id(topic_id)
        if not last_review:
            print(f"Topic ID: {topic_id} doesn't exist")
            return

        today = date.today()
        if (
            date.fromordinal(date.toordinal(today) - 7)
            >= last_review.review_at
        ):
            review = self.db.update_topic(
                topic_id,
                date.fromordinal(
                    date.toordinal(today)
                    + last_review.time_interval.interval
                ),
                last_review.time_interval.id,
            )
            print(f"Next review scheduled for: {review.review_at}.")

        intervals = self.db.get_ord_asc_intervals()

        if last_review.interval_id == intervals[-1].id:
            topic = self.db.get_topic(topic_id)
            if not topic:
                return

            print(
                f"Topic '{topic.name}' has already passed through all review stages"
            )
            return

        next_interval_idx = [
            idx
            for idx in range(len(intervals))
            if intervals[idx].id == last_review.interval_id
        ][0] + 1

        next_interval = intervals[next_interval_idx]

        review = self.db.update_topic(
            topic_id,
            date.fromordinal(
                date.toordinal(today) + next_interval.interval
            ),
            next_interval.id,
        )

        print(f"Next review scheduled for: {review.review_at}.")

    def add(self, topic_name: str):
        topic = self.db.get_topic_by_name(topic_name)
        if topic:
            print(f"{topic_name} already exist.")
            return

        interval = self.db.get_time_interval_by_id(1)
        if not interval:
            print("Database not initialized.")
            return

        topic, review = self.db.add_topic(topic_name, interval)
        print(f"{topic.name}, next review at {review.review_at}.")

    def list(self):
        topics = self.db.list_topics()
        table = tabulate(
            [[t.id, t.name] for t in topics], headers=self.topic_headers
        )
        print(table)

    def get(self, topic_id: int):
        topic = self.db.get_topic(topic_id)
        if not topic:
            print(f"Topic ID: {topic_id} doesn't exist.")
            return

        print(f"{topic.name} reviews:")

        print(
            tabulate(
                [
                    [r.id, r.review_at, r.time_interval.name, r.completed]
                    for r in topic.reviews
                ],
                headers=self.review_headers,
            )
        )

    def delete(self, topic_id: int):
        topic = self.db.delete_topic(topic_id)

        if not topic:
            print(f"Topic ID: {topic_id} doesn't exist.")
            return

        print(f"{topic.name} deleted.")
