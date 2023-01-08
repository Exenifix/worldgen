if __name__ == "__main__":
    import argparse

    from . import World

    parser = argparse.ArgumentParser(
        prog="exenworldgen",
        usage="exenworldgen <size> [worlds]",
        description="Generates a set number of worlds with specified size and prints them in terminal.",
    )
    parser.add_argument("size", metavar="size", type=str, help="Size of the generated world, eg. 50x20")
    parser.add_argument("worlds", metavar="worlds", default=1, type=int, help="Amount of generated worlds", nargs="?")

    args = parser.parse_args()
    size = tuple(map(int, args.size.split("x", maxsplit=1)))
    if len(size) != 2:
        raise TypeError("Bad size. Please input size like 50x20")
    if args.worlds < 1:
        raise TypeError("Please input valid amount of worlds")
    for _ in range(args.worlds):
        world = World(size)  # type: ignore
        world.generate()
        world.print()
