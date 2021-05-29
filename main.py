from typing import Type
from frontends.debugging_frontend import DebuggingFrontend
from frontend_base import BaseFrontend
from controller import GameOfLifeController


def main(desired_frontend: Type[BaseFrontend]):
    controller = GameOfLifeController()
    frontend = desired_frontend(controller)
    controller.set_frontend(frontend)
    controller.run()


if __name__ == "__main__":
    main(DebuggingFrontend)
