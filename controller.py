import sys
from mvc_base import BaseFrontend, BaseController
from game_logic import GameOfLifeEngine, GameState


class GameOfLifeController(BaseController):
    def __init__(self):
        self.view: BaseFrontend
        self.engine = GameOfLifeEngine()
        self.state = GameState()

    def set_frontend(self, frontend: BaseFrontend) -> None:
        self.view = frontend

    def set_state(self, state: GameState) -> None:
        self.state = state

    def handle_request(self, request) -> None:
        if request.type == 'exit':
            self.close()
        elif request.type == 'next':
            game_state = self.engine.calculate_next_game_state(self.state)
            self.set_state(game_state)
            self.view.update(game_state)
        elif request.type == 'update_state':
            self.set_state(getattr(request, 'state'))

    def initialize(self):
        self.view.initialize()
        self.view.show()

    def close(self):
        self.view.close()
        sys.exit()
