from argparse import ArgumentParser
from datetime import date
from typing import Optional
from sys import argv


class CLI:
    def __init__(self):
        self._parser = self._init_parser()

    def _init_parser(self):
        parser = ArgumentParser(
            prog="Review Planner",
            description="Schedule reviews for better fixation.",
        )

        subparsers = parser.add_subparsers()

        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Enable debus options.",
        )

        add = subparsers.add_parser(
            "add", help="Add a new topic, and create first review entry."
        )

        add.add_argument("topic", help="The name of the new topic entry.")

        subparsers.add_parser("lt", help="List all registered topics.")

        lr = subparsers.add_parser("lr", help="List all reviews.")

        lr.add_argument(
            "-t",
            "--today",
            const=date.today(),
            action="store_const",
            help="List reviews from today.",
        )

        lr.add_argument(
            "-d",
            "--date",
            type=str,
            help="List reviews for provided date, which must be in YYYY-MM-DD format",
        )

        lr.add_argument(
            "-c",
            "--completed",
            help="List completed reviews.",
            const=True,
            action="store_const",
        )

        lr.add_argument(
            "-nc",
            "--not-completed",
            help="List not completed reviews.",
            const=False,
            action="store_const",
        )

        update = subparsers.add_parser(
            "update", help="Update review to next stage."
        )
        update.add_argument(
            "topic_id", type=int, help="The id of the topic to update"
        )

        get = subparsers.add_parser(
            "get", help="List topic and review entries"
        )
        get.add_argument(
            "topic_id",
            type=int,
            help="The id of the topic to retrieve information",
        )

        delete = subparsers.add_parser(
            "delete", help="Remove the topic from the review process."
        )
        delete.add_argument(
            "topic_id", type=int, help="The id of the topic to delete."
        )

        return parser

    def parse(self, args: Optional[list[str]] = None):
        if not args:
            args = argv[1:]

        if not args:
            self._parser.parse_args(["-h"])

        namespace = self._parser.parse_args(args)
        namespace.command = args[0] if args[0] != "-d" else args[1]

        return namespace
