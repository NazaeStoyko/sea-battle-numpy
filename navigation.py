def east(row, col):
	return row, col + 1

def west(row, col):
	return row, col - 1

def north(row, col):
	return row - 1, col

def south(row, col):
	return row + 1, col


def east_noeth_east(row, col):
	return north(*east(row, col))

def east_south_east(row, col):
	return south(*east(row, col))


def west_right_center(row, col):
	return row, col + 1

def west_left_center(row, col):
	return row, col - 1


def west_noeth_west(row, col):
	return north(*west(row, col))

def west_south_west(row, col):
	return south(*west(row, col))


def north_east(row, col):
	return east(*north(row, col))

def north_west(row, col):
	return west(*north(row, col))

def south_west(row, col):
	return west(*south(row, col))

def south_east(row, col):
	return east(*south(row, col))