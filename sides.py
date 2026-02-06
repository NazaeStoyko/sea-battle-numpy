import ships
import field as fd


class Sides:
    def __init__(self):
        self.field = fd.Fields()
        self.ship = ships
        self.direction = {
            "up":    (-1, 0),
            "down":  (1, 0),
            "left":  (0, -1),
            "right": (0, 1),}
        self.valid_directions = []

    def check_sides(self, start_row, start_col):
        word_length = 5


        for name, (dr, dc) in self.direction.items():
            cells=[]

            for i in range (word_length):
                r = start_row + dr * i
                c = start_col + dc * i

                # перевірка меж поля
                if r < 0 or r >= self.field.field_bot.shape[0] or c < 0 or c >= self.field.field_bot.shape[1]:
                    break

                cells.append(self.field.field_bot[r, c])

            else:
                # перевірка вмісту клітин
                if all(cell == 0 for cell in cells):
                    self.valid_directions.append(name)

        print(self.valid_directions)

