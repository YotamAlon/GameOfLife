from typing import Type
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from frontends.debugging_frontend import DebuggingFrontend
from frontend_base import BaseFrontend
from controller import GameOfLifeController


def main(desired_frontend: Type[BaseFrontend], log_level: str):
    logger = getLogger()
    logger.setLevel(log_level)
    controller = GameOfLifeController()
    frontend = desired_frontend(controller)
    controller.set_frontend(frontend)
    controller.run()


if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser('CLI interface for Conway\'s game of life')
    arg_parser.add_argument('-l', '--log-level', options=[DEBUG, INFO, WARNING, ERROR, CRITICAL], default=WARNING)
    args = arg_parser.parse_args()

    main(DebuggingFrontend, args.log_level)
