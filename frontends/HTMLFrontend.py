import os
import signal
from flask import Flask, redirect, url_for, request
from tabulate import tabulate
from mvc_base import BaseFrontend, BaseModel


class HTMLFrontend(BaseFrontend):
    def initialize(self, initial_state: BaseModel) -> None:
        self.view_state = initial_state
        self.app = Flask(__name__)

        @self.app.route('/')
        def index():
            grid = self.generate_grid(self.view_state)
            return tabulate([[f'{y}'] + [self.turn_on_button(cell) for cell in grid[i]]
                             for i, y in enumerate(self.view_state.y_range)],
                            headers=[' '] + [f'{x}' for x in self.view_state.x_range], tablefmt='unsafehtml')\
                + self.bottom_buttons()

        @self.app.route('/set/<string:coordinates>')
        def set_(coordinates: str):
            x, y = coordinates.split(',')
            self.controller.update_cell(int(x), int(y), is_alive=True)
            return redirect(url_for('index'))

        @self.app.route('/next')
        def next_():
            self.controller.next()
            return redirect(url_for('index'))

        @self.app.route('/exit')
        def close():
            self.controller.exit()
            return redirect(url_for('index'))

    @staticmethod
    def generate_grid(game_state: BaseModel):
        return [[game_state.get_cell(x, y) for x in game_state.x_range] for y in game_state.y_range]

    @staticmethod
    def turn_on_button(cell):
        return f'<a href="/set/{cell.x},{cell.y}">{"■" if cell.is_alive else "□"}</a>'

    @staticmethod
    def bottom_buttons():
        return '<a href="/next">Next</a> <a href="/exit">Close</a>'

    def update(self, state: BaseModel) -> None:
        self.view_state = state

    def show(self) -> None:
        self.app.run(debug=True)

    def close(self) -> None:
        os.kill(os.getpid(), signal.SIGINT)
