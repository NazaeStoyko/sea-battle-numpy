import field as fd
import random


def main():
    field_user = fd.Field()

    for _ in range(1):
        coordinates = field_user.random_coordinats()
        # row, col = field_user.parse_place(coordinates)
        row, col = 0,6
        where_to_draw = field_user.where_to_draw(row, col, 3)
        
        if where_to_draw is not None:
            ship_direction, direction = where_to_draw
            
            field_user.draw_ship(row, col, 3, ship_direction, direction)
            print("\n")
            
            print(field_user.field)


            # symbols = {0: ".", 1: "■"}
            # size = field_user.field.shape[1]
            # print("   " + " ".join(f"{i}" for i in range(size)))
            # for i, row in enumerate(field_user.field):
            #     print(f"{i:2} " + " ".join(symbols[cell] for cell in row))

        else:

            print("Ship is not valid")



if __name__ == "__main__":
    main()