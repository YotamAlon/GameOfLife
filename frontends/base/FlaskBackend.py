import os
import signal
from flask import Flask, render_template, redirect, url_for
from mvc_base import BaseFrontend, BaseModel


class FlaskBackend(BaseFrontend):
    @property
    def urls(self):
        return {'/': self.index, '/set/<string:coordinates>': self.set_, '/next': self.next_,
                '/exit': self.exit}

    @property
    def html_template(self):
        raise NotImplementedError()

    def initialize(self, initial_state: BaseModel) -> None:
        self.view_state = initial_state
        self.app = Flask(self.__module__)
        for url, func in self.urls.items():
            self.app.route(url)(func)

    def get_index_data(self):
        raise NotImplementedError()

    def index(self):
        data = self.get_index_data()
        return render_template(self.html_template, **data)

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

    def update(self, state: BaseModel) -> None:
        self.view_state = state

    def show(self) -> None:
        self.app.run(debug=True)

    def close(self) -> None:
        os.kill(os.getpid(), signal.SIGINT)
