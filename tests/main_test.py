import os

from exenworldgen import World


def test_main():
    world = World((25, 25))
    world.generate()
    print()
    world.print()


def test_cli():
    os.system("python -m exenworldgen 10x10 15")
