import logging
from typing import Type
from frontends.CLIFrontend import CLIFrontend
from models.MemoryModel import MemoryState
from models.SQLiteModel import SQLiteState
from mvc_base import BaseFrontend, BaseModel
from controller import GameOfLifeController


def main(desired_frontend: Type[BaseFrontend], desired_model: Type[BaseModel], log_level: str):
    logging.basicConfig(level=getattr(logging, log_level))
    logging.info(f'log level was set to {log_level}')
    controller = GameOfLifeController(model=desired_model, view=desired_frontend)
    controller.initialize()


if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser('CLI interface for Conway\'s game of life')
    arg_parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                            default='WARNING')
    args = arg_parser.parse_args()

    main(CLIFrontend, SQLiteState, args.log_level)
