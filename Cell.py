class Cell:
    NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 1),
                        (1, -1), (1, 0), (1, 1)]
    birth = [2, 3]
    survive = [3]
    def __init__(self, x, y, is_alive=False):
        self.x = x
        self.y = y
        self.is_alive = is_alive
        self.will_be_alive = is_alive


    def count_alive_neighbours(self, cell_list):
        count = 0
        for dx, dy in Cell.NEIGHBOR_OFFSETS:
        
            nx = (self.x + dx) % len(cell_list)
            ny = (self.y + dy) % len(cell_list[0])
            if cell_list[nx][ny].is_alive:
                count += 1
        return count

    def calculate_cell_state(self, cell_list):
        alive_count = self.count_alive_neighbours(cell_list)

        if self.is_alive:
            self.will_be_alive = alive_count in Cell.birth  # 2 or 3 live neighbors otherwise dies
        else:
            self.will_be_alive = alive_count in Cell.survive  # if dead, revives with 3 neighbors

    @staticmethod
    def change_rules(birth, survive):
        Cell.birth = birth
        Cell.survive = survive

    def update(self):
        self.is_alive = self.will_be_alive

    def __repr__(self):
        return "⬛" if self.is_alive else "⬜"