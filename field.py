import numpy as np
from enum import Enum
import random

from numpy.ma.extras import compress_cols


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
        self.idx = np.random.randint(len(self.allowed_places))
        return self.allowed_places[self.idx]

    def parse_place(self, place):
        start_row = place // 10
        start_col = place % 10
        return start_row, start_col

    def unparse_place(self, start_row, start_col):
        start_row * 10 + start_col
        return  start_row * 10 + start_col


    def draw_cell(self, start_row, start_col):
        self.field[start_row, start_col] = 1
        self.delete_allowed_places(start_row, start_col)

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

            elif direction == Direction.South:
                for i in range(length):
                    if self.field[start_row + i, start_col] != 0:
                        return False
                return True
            else:
                return False

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
                    self.draw_cell(start_row, start_col - i)


    def where_to_draw(self, start_row, start_col, length):
        directions = [
            (ShipDirection.Horizontal, Direction.West),
            (ShipDirection.Horizontal, Direction.East),
            (ShipDirection.Vertical, Direction.North),
            (ShipDirection.Vertical, Direction.South),
        ]

        valid_directions = []

        for ship_direction, direction in directions:
            if (
                    self.validate_ship_size(start_row, start_col, length, ship_direction, direction)
                    and
                    self.validate_ship_place(start_row, start_col, length, ship_direction, direction)
            ):
                valid_directions.append((ship_direction, direction))

        if not valid_directions:
            return None

        return random.choice(valid_directions)

    def draw_ship(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction,
    ):

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

    # def scaner():
    #return None
    
    # def create_scope(self, row, col):
    #     row0 = max(0, row - 1)
    #     row1 = min(self.field.shape[0], row + 2)
    #     col0 = max(0, col - 1)
    #     col1 = min(self.field.shape[1], col + 2)
    #
    #     for i in range(row0, row1):
    #         for j in range(col0, col1):
    #             if (i, j) != (row, col):
    #                 self.field[i, j] = 2
    
    

    def delete_allowed_places(self, row, col):
        unparse_coordinates = self.unparse_place(row, col)
        ind = np.where(self.allowed_places == unparse_coordinates)
        
        # row0 = max(0, row - 1)
        # row1 = min(self.field.shape[0], row + 2)
        # col0 = max(0, col - 1)
        # col1 = min(self.field.shape[1], col + 2)
        #
        # for i in range(row0, row1):
        #     for j in range(col0, col1):
        #         if (i, j) != (row, col):
        #             self.field[i, j] = 2

        self.allowed_places =  np.delete(self.allowed_places,ind)
        print("Delete allowed coordinates: unparse_coordinates:", unparse_coordinates)
        print("allowed_places deleted: ", self.allowed_places)
        print("\t")
        return self.allowed_places
