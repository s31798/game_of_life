
class GameState:
    def __init__(self, initial_state):
        self.state = initial_state
    def update(self):
        for row in self.state:
            for cell in row:
                cell.calculate_cell_state(self.state)
                cell.update()