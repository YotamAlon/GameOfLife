import logging
from typing import Type
from frontends.debugging_frontend import CLIFrontend
from frontend_base import BaseFrontend
from controller import GameOfLifeController


def main(desired_frontend: Type[BaseFrontend], log_level: str):
    logging.basicConfig(level=getattr(logging, log_level))
    logging.info(f'log level was set to {log_level}')
    controller = GameOfLifeController()
    frontend = desired_frontend(controller)
    controller.set_frontend(frontend)
    controller.run()


if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser('CLI interface for Conway\'s game of life')
    arg_parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                            default='WARNING')
    args = arg_parser.parse_args()

    main(CLIFrontend, args.log_level)
