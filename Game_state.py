import copy


class GameState:
    def __init__(self, initial_state):
        self.initial_state = copy.deepcopy(initial_state)
        self.state = initial_state

    def make_cell_alive(self, x, y):

        if 0 <= y < len(self.state) and 0 <= x < len(self.state[0]):
            cell = self.state[y][x]
            cell.is_alive = True
        else:
            raise IndexError(f"Cell coordinates ({x}, {y}) out of bounds.")


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