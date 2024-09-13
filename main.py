from cli import CLI
from db import Database

if __name__ == "__main__":
    db = Database()
    db._init_time_intervals()

    cli = CLI()
    namespace = cli.parse()
    print(namespace)
