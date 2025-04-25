class Cell:
    NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 1),
                        (1, -1), (1, 0), (1, 1)]

    def __init__(self, x, y, is_alive=False):
        self.x = x
        self.y = y
        self.is_alive = is_alive
        self.will_be_alive = is_alive

    def count_alive_neighbours(self, cell_list):
        return sum(
            0 <= self.x + dx < len(cell_list)
            and 0 <= self.y + dy < len(cell_list[0])
            and cell_list[self.x + dx][self.y + dy].is_alive
            for dx, dy in Cell.NEIGHBOR_OFFSETS)

    def calculate_cell_state(self, cell_list):
        alive_count = self.count_alive_neighbours(cell_list)

        if self.is_alive:
            self.will_be_alive = alive_count in [2, 3]  # 2 or 3 live neighbors otherwise dies
        else:
            self.will_be_alive = alive_count == 3  # if dead, revives with 3 neighbors

    def update(self):
        self.is_alive = self.will_be_alive

    def __repr__(self):
        return "⬛" if self.is_alive else "⬜"