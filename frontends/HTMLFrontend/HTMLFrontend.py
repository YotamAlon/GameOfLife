from frontends.base.FlaskBackend import FlaskBackend
from mvc_base import BaseModel


class HTMLFrontend(FlaskBackend):
    @property
    def html_template(self):
        return 'index.html'

    def get_index_data(self):
        grid = self.generate_grid(self.view_state)
        data = {'grid': grid, 'x_range': self.view_state.x_range, 'y_range': self.view_state.y_range}
        return data

    @staticmethod
    def generate_grid(game_state: BaseModel):
        return [[game_state.get_cell(x, y) for x in game_state.x_range] for y in game_state.y_range]
