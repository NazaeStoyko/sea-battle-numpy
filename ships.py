import random

import numpy as np
import field as fd
import sides as sides

# Мало б працювати як розставлення сторін тільки є пару дефектів


class ArrangementShip:
    def __init__(self):
        self.idx = None
        self.start_row = None
        self.start_col = None
        self.field = fd.Fields()
        self.sides.Sides()
        self.palce = np.arange(0, 100)

    def random_coordinats(self):

        self.idx = np.random.randint(len(self.palce))
        random_choices = self.palce[self.idx]
        start_row = random_choices // 10
        start_col = (random_choices % 10)
        self.sent_check_side(start_row,start_col)

    def sent_check_side(self,start_row,start_col):

        self.side.check_sides(start_row , start_col)


        # random_choices_sides = random.choices(list(self.side.direction.keys()))
        # print(random_choices_sides)


    # def draw_ship(self, valid_directions):
    #     print(valid_directions)







        # print(self.field.field_user)
        # print(self.can_side)

        # self.field.field_user[5][5] = 1
        # print(self.field.field_user)
        # print(self.field.field_user[5][5])


a = ArrangementShip()
a.random_coordinats()
