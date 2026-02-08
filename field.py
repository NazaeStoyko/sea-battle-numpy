import numpy as np
from enum import Enum


class ShipDirection(Enum):
    Vertical = "V"
    Horizontal = "H"


class Direction(Enum):
    North = "N"
    East = "E"
    West = "W"
    South = "S"


class Field:

    def __init__(self):
        self.field = np.zeros(shape=(10, 10), dtype=int)
        self.allowed_places = np.arange(0, 100)

    def random_coordinats(self):
        self.idx = np.random.randint(len(self.palce))
        random_choices = self.allowed_places[self.idx]

    def parse_place(self, place):
        start_row = place // 10
        start_col = place % 10
        return start_row, start_col

    def unparse_place(self, start_row, start_col):
        return start_row * 10 + start_col

    def draw_cell(self, start_row, start_col):
        self.field[start_row, start_col] = 1

    # Check wether ship size fits the field
    def validate_ship_size(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction,
    ):

        if ship_direction == ShipDirection.Vertical:
            if direction == Direction.North:
                return start_row + 1 - length >= 0

            if direction == Direction.South:
                return start_row - 1 + length <= 9
            else:
                return False


# Problem with return start_col - 1 + length <= 10
        elif ship_direction == ShipDirection.Horizontal:
            if direction == Direction.East:
                return start_col + 1 + length <= 11

            if direction == Direction.West:
                return start_col - 1 - length >= 0

            else:
                return False
        else:
            return False

    def validate_ship_place(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction,
    ):
        if ship_direction == ShipDirection.Vertical:
            if direction == Direction.North:
                for i in range(length):
                    if self.field[start_row - i, start_col] != 0:
                        return False
                return True
# Here is "index 10 is out of bounds for axis 1 with size 10"
            elif direction == Direction.South:
                for i in range(length):
                    if self.field[start_row + i, start_col] != 0:
                        return False
                return True
            else:
                return False
# Here is "index 10 is out of bounds for axis 1 with size 10"
        elif ship_direction == ShipDirection.Horizontal:
            if direction == Direction.East:
                for i in range(length):
                    if self.field[start_row, start_col + i] != 0:
                        return False
                return True
            elif direction == Direction.West:
                for i in range(length):
                    if self.field[start_row, start_col - i] != 0:
                        return False
                return True
            else:
                return False

    def unsafe_draw_ship(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction,
    ):
        if ship_direction == ShipDirection.Vertical:
            if direction == Direction.North:
                for i in range(length):
                    self.draw_cell(start_row - i, start_col)
            elif direction == Direction.South:
                for i in range(length):
                    self.draw_cell(start_row + i, start_col)
        elif ship_direction == ShipDirection.Horizontal:
            if direction == Direction.East:
                for i in range(length):
                    self.draw_cell(start_row, start_col + i)
            elif direction == Direction.West:
                for i in range(length):
                    print("Drawing cell:", start_row, start_col - i)
                    self.draw_cell(start_row, start_col - i)
        # self.delete_allowed_places(row, col)

    def draw_ship(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction,
    ):
        # print("Drawing ship...")
        # print("Start row:", start_row, "Start col:", start_col)
        # print(
        #     "validate size:",
        #     self.validate_ship_size(
        #         start_row, start_col, length, ship_direction, direction
        #     ),
        # )
        # print(
        #     "validate place:",
        #     self.validate_ship_place(
        #         start_row, start_col, length, ship_direction, direction
        #     ),
        # )
        if self.validate_ship_size(
            start_row, start_col, length, ship_direction, direction
        ) and self.validate_ship_place(
            start_row, start_col, length, ship_direction, direction
        ):
            self.unsafe_draw_ship(
                start_row, start_col, length, ship_direction, direction
            )
            return True
        else:
            print("Ship is not valid")
            return False

    def delete_allowed_places(self, row, col):
        return None
