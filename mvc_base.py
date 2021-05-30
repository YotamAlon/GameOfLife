from game_logic import GameState


class Request(object):
    def __init__(self, type_):
        self.type = type_


class BaseController(object):
    def set_frontend(self, frontend) -> None:
        """Initial function to set the desired frontend"""
        raise NotImplementedError()

    def handle_request(self, request: Request) -> None:
        """Handle Requests coming from the view"""
        raise NotImplementedError()

    def close(self) -> None:
        """Close and cleanup"""
        raise NotImplementedError()


class BaseFrontend(object):
    def __init__(self, controller: BaseController):
        self.controller = controller
        self.view_state: GameState

    def show(self) -> None:
        """The main function of the view"""
        raise NotImplementedError()

    def update(self, state: GameState) -> None:
        """Update the view state with the latest game state"""
        raise NotImplementedError()

    def initialize(self) -> None:
        """Initialze the view"""
        raise NotImplementedError()

    def close(self) -> None:
        """Close and cleanup"""
        raise NotImplementedError()
