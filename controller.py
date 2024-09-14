from db import Database
from tabulate import tabulate

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

    def update(self, topic_id: int):
        review = self.db.update_topic(topic_id)
        if not review:
            print("No review created.")
            return
        print(f"Next review scheduled for: {review}.")

    def add(self, topic_name: str):
        topic_id = self.db.add_topic(topic_name)
        if topic_id:
            print(f"{topic_name} created. ID: {topic_id}.")
            return
        print(f"{topic_name} already exist.")

    def list(self):
        topics = self.db.list_topics()
        table = tabulate(
            [
                [t.id, t.name] for t in topics
            ],
            headers=self.topic_headers
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
                    [
                        r.id,
                        r.review_at,
                        r.time_interval.name,
                        r.completed
                    ] for r in topic.reviews
                ],
                headers=self.review_headers
            )
        )

    def delete(self, topic_id: int):
        topic = self.db.delete_topic(topic_id)

        if not topic:
            print(f"Topic ID: {topic_id} doesn't exist.")
            return

        print(f"{topic.name} deleted.")
