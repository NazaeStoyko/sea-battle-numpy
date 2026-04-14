import numpy as np
import random
import navigation
from enum import IntEnum
from enum import Enum


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
		return start_row * 10 + start_col
	
	def draw_cell(self, start_row, start_col, kind):
		
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
				return start_row - (length - 1) >= 0
			
			if direction == Direction.South:
				return start_row + (length - 1) < 10
			else:
				return False
		
		elif ship_direction == ShipDirection.Horizontal:
			if direction == Direction.East:
				return start_col + (length - 1) < 10
			
			if direction == Direction.West:
				return start_col - (length - 1) >= 0
			
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
			direction: Direction
	):
		kind = "ship"
		
		if ship_direction == ShipDirection.Vertical:
			if direction == Direction.North:
				for i in range(length):
					self.draw_cell(start_row - i, start_col, kind)
			
			elif direction == Direction.South:
				for i in range(length):
					self.draw_cell(start_row + i, start_col, kind)
		
		elif ship_direction == ShipDirection.Horizontal:
			if direction == Direction.East:
				for i in range(length):
					self.draw_cell(start_row, start_col + i, kind)
			
			elif direction == Direction.West:
				for i in range(length):
					self.draw_cell(start_row, start_col - i, kind)
	
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
			
			self.draw_borders(
				start_row, start_col, length, ship_direction, direction
			)
			
			return True
		else:
			print("Ship is not valid")
			return False
	
	def draw_borders(self, row, col, length, ship_direction, direction):
		
		if ship_direction == ShipDirection.Horizontal:
			for i in range(length):
				
				if direction == Direction.West:
					r = row
					c = col - i
				
				if direction == Direction.East:
					r = row
					c = col + i
				
				if 0 <= r < 10 and 0 <= c < 10:
					
					for func in [
						navigation.north,
						navigation.south,
						navigation.west,
						navigation.east,
						navigation.north_west,
						navigation.north_east,
						navigation.south_west,
						navigation.south_east
					]:
						horizontal_row, horizontal_col = func(r, c)
						if 0 <= horizontal_row < 10 and 0 <= horizontal_col < 10:
							if self.field[horizontal_row, horizontal_col] == CellType.Empty:
								self.draw_cell(horizontal_row, horizontal_col, kind="border")
		
		if ship_direction == ShipDirection.Vertical:
			for i in range(length):
				
				if direction == Direction.North:
					r = row - i
					c = col
				
				if direction == Direction.South:
					r = row + i
					c = col
				
				if 0 <= r < 10 and 0 <= c < 10:
					
					for func in [
						navigation.north,
						navigation.south,
						navigation.west,
						navigation.east,
						navigation.north_west,
						navigation.north_east,
						navigation.south_west,
						navigation.south_east
					]:
						nr, nc = func(r, c)
						if 0 <= nr < 10 and 0 <= nc < 10:
							if self.field[nr, nc] == CellType.Empty:
								self.draw_cell(nr, nc, kind="border")
	
	def delete_allowed_places(self, row, col):
		unparse_coordinates = self.unparse_place(row, col)
		ind = np.where(self.allowed_places == unparse_coordinates)
		
		self.allowed_places = np.delete(self.allowed_places, ind)
		
		# print("Delete allowed coordinates:", unparse_coordinates)
		# print("allowed_places:", self.allowed_places)
		
		
		
		return self.allowed_places