import field as fd
import random


def main():
    field_user = fd.Field()

    for _ in range(2):
        coordinates = field_user.random_coordinats()
        row, col = field_user.parse_place(coordinates)
        where_to_draw = field_user.where_to_draw(row, col, 2)
        if where_to_draw is not None:
            ship_direction, direction = where_to_draw
            field_user.draw_ship(row, col, 2, ship_direction, direction)

            # print("allowed_places deleted: ",field_user.allowed_places)
            print("\n")
            print(field_user.field)



        else:
            print("Ship is not valid")



if __name__ == "__main__":
    main()