import field as fd
import shot_bot as sb


def print_fields(user_field, bot_field):
    field_size = len(user_field.field)
    cell_width = 2

    def build_header():
        return " " * (cell_width + 1) + " ".join(f"{i:>{cell_width}}" for i in range(field_size))

    def build_border():
        return " " * (cell_width) + "+" + "+".join(["-" * cell_width] * field_size) + "+"

    def hide_bot_ships(cell_value):
        if cell_value in (1, 2):   # приховує і кораблі і їх межі
            return 0
        return cell_value

    def build_row(row_index, row_data, hide=False):
        if hide:
            row_data = [hide_bot_ships(cell) for cell in row_data]
        return f"{row_index:>{cell_width}}|" + "|".join(f"{cell:>{cell_width}}" for cell in row_data) + "|"

    gap_between_fields = "  "

    header = build_header()
    border = build_border()

    print("USER".center(len(header)) + gap_between_fields + "BOT".center(len(header)))
    print(header + gap_between_fields + header)
    print(border + gap_between_fields + border)

    for row_index, (user_row, bot_row) in enumerate(zip(user_field.field, bot_field.field)):
        print(build_row(row_index, user_row) + gap_between_fields + build_row(row_index, bot_row, hide=True))
        print(border + gap_between_fields + border)


def get_user_input():
    row = int(input("row: "))
    col = int(input("col: "))
    return row, col


def place_ships(field, ships_config):
    for ship_count, ship_length in ships_config.items():
        for _ in range(ship_count):
            while True:
                coordinates = field.random_coordinats()
                row, col = field.parse_place(coordinates)

                possible = field.where_to_draw(row, col, ship_length)
                if possible is not None:
                    ship_direction, direction = possible
                    field.draw_ship(row, col, ship_length, ship_direction, direction)
                    break


def main():
    user_field = fd.Field()
    bot_field = fd.Field()

    ships_config = {1: 4, 2: 3, 3: 2, 4: 1}
    total_ship_cells = sum(count * length for count, length in ships_config.items())

    place_ships(user_field, ships_config)
    place_ships(bot_field, ships_config)

    bot_shooter = sb.GetCoordinates()

    user_hits = 0
    bot_hits = 0

    while True:
        print_fields(user_field, bot_field)

        # USER TURN
        while True:
            row, col = get_user_input()
            if bot_field.field[row][col] not in (3, 4):
                break

        if bot_field.field[row][col] == 1:
            bot_field.field[row][col] = 4
            user_hits += 1
            print("HIT")
        else:
            bot_field.field[row][col] = 3
            print("MISS")

        if user_hits == total_ship_cells:
            print("USER WIN")
            break

        # BOT TURN (поки попадає)
        while True:
            while True:
                row, col = bot_shooter.creatShotCoordinates()
                if user_field.field[row][col] not in (3, 4):
                    break

            print("Хід супротивника:", row, col)

            if user_field.field[row][col] == 1:
                user_field.field[row][col] = 4
                bot_hits += 1
                print("BOT HIT")

                if bot_hits == total_ship_cells:
                    print("BOT WIN")
                    return
            else:
                user_field.field[row][col] = 3
                print("BOT MISS")
                break


if __name__ == "__main__":
    main()