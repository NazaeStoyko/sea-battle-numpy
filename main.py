import field as fd


def main():
    field_user = fd.Field()
    field_user.draw_ship(5, 5, 7, fd.ShipDirection.Horizontal, fd.Direction.East)

    print(field_user.field)


if __name__ == "__main__":
    main()
