from cli import CLI
from controller import Controller
from db import Database

if __name__ == "__main__":
    db = Database()
    db._init_time_intervals()

    controller = Controller(db)
    cli = CLI()
    namespace = cli.parse()
    match namespace.command:
        case "add":
            controller.add(namespace.topic)
        case "get":
            controller.get(namespace.topic_id)
        case "list":
            controller.list()
        case "delete":
            controller.delete(namespace.topic_id)
        case "update":
            controller.update(namespace.topic_id)
        case _:
            print(f"{namespace.command} doesn't exist")
