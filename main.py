import field as fd


def print_fields(field_user, field_bot):
    size = len(field_user.field)
    cell_w = 3

    def header():
        
        return " " * (cell_w + 2) + "".join(f"{i:^{cell_w+2}}" for i in range(size))

    def border():
        return " " * (cell_w + 1) + "+" + "+".join(["-" * (cell_w+1)] * size) + "+"

    def row(i, data):
        return f"{i:>{cell_w}} " + "|" + "|".join(f"{cell:^{cell_w+1}}" for cell in data) + "|"

    gap = "    "

    print("USER FIELD".center(len(header())) + gap + "BOT FIELD".center(len(header())))
    print(header() + gap + header())
    print(border() + gap + border())

    for row_index, (user_row, bot_row) in enumerate(zip(field_user.field, field_bot.field)):
        print(row(row_index, user_row) + gap + row(row_index, bot_row))
        print(border() + gap + border())

def main():
    field_user = fd.Field()
    field_bot = fd.Field()
    ships = {1:4, 2: 3, 3: 2, 4: 1}
    
    for field in (field_user, field_bot):
        for key, value in ships.items():
            for _ in range(key):
                coordinates = field.random_coordinats()
                row, col = field.parse_place(coordinates)
    
                length = value
                where_to_draw = field.where_to_draw(row, col, length)
                
                if where_to_draw is not None:
                    ship_direction, direction = where_to_draw
                    
                    field.draw_ship(row, col, length, ship_direction, direction)
                    
                else:
      
                    print("Ship is not valid")
    
    print_fields(field_user, field_bot)

if __name__ == "__main__":
    main()