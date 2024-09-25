from datetime import date
from cli import CLI
from controller import Controller
from db import Database

if __name__ == "__main__":
    cli = CLI()
    namespace = cli.parse()

    db = Database(namespace.debug)
    db._init_time_intervals()
    controller = Controller(db)

    match namespace.command:
        case "add":
            controller.add(namespace.topic)
        case "get":
            controller.get(namespace.topic_id)
        case "lt":
            controller.list()
        case "lr":
            if namespace.today:
                controller.list_reviews_from_date(namespace.today)
            elif namespace.date:
                controller.list_reviews_from_date(
                    date.fromisoformat(namespace.date)
                )
            elif namespace.completed:
                controller.list_reviews_from_completed(namespace.completed)
            elif namespace.not_completed is not None:
                controller.list_reviews_from_completed(
                    namespace.not_completed
                )
            else:
                controller.list_revies()
        case "delete":
            controller.delete(namespace.topic_id)
        case "update":
            controller.update(namespace.topic_id)
        case _:
            print(f"{namespace.command} doesn't exist")
