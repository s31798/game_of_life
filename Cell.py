class Cell:
    def __init__(self, x, y, is_alive=False):
        self.x = x
        self.y = y
        self.is_alive = is_alive
        self.will_be_alive = is_alive

    def count_alive_neighbours(self, cell_list):
        alive_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue #skip self
                neighbour_x, neighbour_y = self.x + i, self.y + j
                if 0 <= neighbour_x <= len(cell_list) and 0 <= neighbour_y <= len(cell_list[0]):
                    if cell_list[neighbour_x][neighbour_y].is_alive:
                        alive_count += 1
        return alive_count

    def calculate_cell_state(self, cell_list):
        alive_count = self.count_alive_neighbours(cell_list)

        if self.is_alive:
            self.will_be_alive = alive_count in [2, 3]  # 2 or 3 live neighbors otherwise dies
        else:
            self.will_be_alive = alive_count == 3 # if dead, revives with 3 neighbors

    def update(self):
        self.is_alive = self.will_be_alive
