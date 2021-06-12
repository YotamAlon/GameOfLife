import os
import signal
from flask import Flask, redirect, url_for, render_template
from tabulate import tabulate
from mvc_base import BaseFrontend, BaseModel


class HTMLFrontend(BaseFrontend):
    def initialize(self, initial_state: BaseModel) -> None:
        self.view_state = initial_state
        self.app = Flask(__name__)
        for url, func in self.urls.items():
            self.app.route(url)(func)

    @property
    def html_template(self):
        return 'index.html'

    @property
    def urls(self):
        return {'/': self.index, '/set/<string:coordinates>': self.set_, '/next': self.next_,
                '/exit': self.exit}

    def index(self):
        data = self.get_index_data()
        return render_template(self.html_template, **data)

    def get_index_data(self):
        grid = self.generate_grid(self.view_state)
        data = {'grid': grid, 'x_range': self.view_state.x_range, 'y_range': self.view_state.y_range}
        return data

    def set_(self, coordinates: str):
        x, y = coordinates.split(',')
        self.controller.update_cell(int(x), int(y), is_alive=True)
        return redirect(url_for('index'))

    def next_(self):
        self.controller.next()
        return redirect(url_for('index'))

    def exit(self):
        self.controller.exit()
        return redirect(url_for('index'))

    @staticmethod
    def generate_grid(game_state: BaseModel):
        return [[game_state.get_cell(x, y) for x in game_state.x_range] for y in game_state.y_range]

    def update(self, state: BaseModel) -> None:
        self.view_state = state

    def show(self) -> None:
        self.app.run(debug=True)

    def close(self) -> None:
        os.kill(os.getpid(), signal.SIGINT)
