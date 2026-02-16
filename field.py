from curses import start_color

import numpy as np
import random
import navigation
from enum import IntEnum
from enum import Enum
from numpy.ma.extras import compress_cols

class CellType(IntEnum):
    Empty = 0
    Ship = 1
    Border = 2
    Damaged = 3
    
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


    def draw_cell(self, start_row, start_col,kind):
     
        
    
        if kind == "ship":
            self.field[start_row, start_col] = CellType.Ship
        if kind == "border":
            self.field[start_row, start_col] = CellType.Border
            
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
                return start_row - 1 + length <= 10
            else:
                return False

        elif ship_direction == ShipDirection.Horizontal:
            if direction == Direction.East:
                return start_col + 1 + length <= 10

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
        return None
    
    def unsafe_draw_ship(
        self,
        start_row,
        start_col,
        length,
        ship_direction: ShipDirection,
        direction: Direction
    ):
        kind = "ship"
        if ship_direction == ShipDirection.Vertical:
            if direction == Direction.North:
                for i in range(length):
                    self.draw_cell(start_row - i, start_col,kind)
            elif direction == Direction.South:
                for i in range(length):
                    self.draw_cell(start_row + i, start_col,kind)
        elif ship_direction == ShipDirection.Horizontal:
            if direction == Direction.East:
                for i in range(length):
                    self.draw_cell(start_row, start_col + i,kind)
            elif direction == Direction.West:
                for i in range(length):
                    self.draw_cell(start_row, start_col - i,kind)


    def where_to_draw(self, start_row, start_col, length):
        directions = [
            (ShipDirection.Horizontal, Direction.West),
            # (ShipDirection.Horizontal, Direction.East),
            # (ShipDirection.Vertical, Direction.North),
            # (ShipDirection.Vertical, Direction.South),
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
            self.draw_borders(start_row, start_col, length, ship_direction, direction)
            return True
        else:
            print("Ship is not valid")
            return False



    def draw_borders(self, row,col, length,  ship_direction, direction):
       
        if ship_direction == ShipDirection.Horizontal:
            if direction == Direction.West:
                
                if  self.validate_ship_size(row - 1, col, length, ship_direction, direction) == True:
                    for i in range(length):
                        self.draw_cell(*navigation.west_noeth_west(row, col - i), kind="border")
                        
                if self.validate_ship_size(row + 1, col, length, ship_direction, direction) == True:
                    for i in range(length):
                        self.draw_cell(*navigation.west_south_west(row, col-i), kind="border")
                    #     start_row,start_col= navigation.north(row, col-i)
                    #     self.draw_cell(start_row, start_col, kind="border")
                    # if row < 9:
                    #     start_row, start_col = navigation.south(row, col-i)
                    #     self.draw_cell(start_row, start_col, kind="border")
                        
                        
                        
                        
                    # if col < 9:
                    #     if i == 0:
                    #         start_row, start_col = navigation.west_right_center(row, col - i)
                    #         self.draw_cell(start_row, start_col, kind="border")
                    # if col > 0:
                    #     if i+1 == length:
                    #         start_row, start_col = navigation.west_left_center(row, col - i)
                    #         self.draw_cell(start_row, start_col, kind="border")
                    # if row <9 and col < 9:
                    #     if i == 0:
                    #         start_row, start_col = navigation.east_south_east(row, col)
                    #         self.draw_cell(start_row, start_col, kind="border")
                    # if col > 0 and row > 0:
                    #     if i+1 == length:
                    #         start_row, start_col = navigation.west_noeth_west(row, col-i)
                    #         self.draw_cell(start_row, start_col, kind="border")
                    #
                    # if col > 0 and row < 9:
                    #     if i + 1 == length:
                    #         start_row, start_col = navigation.west_south_west(row, col-i)
                    #         self.draw_cell(start_row, start_col, kind="border")
                    # if col < 9 and row > 0:
                    #     if i + 1 == length:
                    #         if i == 0:
                    #             start_row, start_col = navigation.east_noeth_east(row, col)
                    #             self.draw_cell(start_row, start_col, kind="border")
                    
                    
                    
            if direction == Direction.East:
                if row>0:
                    start_row, start_col = navigation.east_noeth_east(row, col)
                    self.draw_cell(start_row, start_col, kind="border")
                if row<9:
                    start_row, start_col = navigation.east_south_east(row, col)
                    self.draw_cell(start_row, start_col, kind="border")
                if col > 0:
                    
                    start_row, start_col = navigation.west_center(row, col)
                    self.draw_cell(start_row, start_col, kind="border")
                if col<9:
                    start_row, start_col = navigation.west_center(row, col)
                    self.draw_cell(start_row, start_col, kind="border")


    

    def delete_allowed_places(self, row, col):
        unparse_coordinates = self.unparse_place(row, col)
        ind = np.where(self.allowed_places == unparse_coordinates)

        self.allowed_places =  np.delete(self.allowed_places,ind)
        print("Delete allowed coordinates: unparse_coordinates:", unparse_coordinates)
        print("allowed_places deleted: ", self.allowed_places)
        print("\t")
        return self.allowed_places
