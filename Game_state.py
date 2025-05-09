import copy


class GameState:
    def __init__(self, initial_state):
        self.initial_state = copy.deepcopy(initial_state)
        self.state = initial_state

    def update(self):
        for row in self.state:
            for cell in row:
                cell.calculate_cell_state(self.state)

        for row in self.state:
            for cell in row:
                cell.update()

    def reset(self):
        self.state = copy.deepcopy(self.initial_state)

    def __repr__(self):
        representation = ""
        for row in self.state:
            row_str = " , ".join(str(cell) for cell in row)
            representation += row_str + "\r"
        return representation