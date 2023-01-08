import random
import sys
import time
from typing import Sequence, TypeVar

from exencolor import Color, colored

Vector2 = tuple[int, int]
T = TypeVar("T")


def random_amount(population: Sequence[T], maxk: int) -> list[T]:
    k = random.randint(0, maxk)
    if k == 0:
        return []
    return random.sample(population, k=k)


class World:
    def __init__(self, size: Vector2):
        self.size = size
        self._data: list[list[int]] = [
            [1] + [0] * (self.size[0] - 2) + [1] for _ in range(self.size[1] - 2)
        ]
        self._data.insert(0, [1] * self.size[0])
        self._data.append([1] * self.size[0])
        self.walls: set[Vector2] = set()
        self.walls |= {(0, i) for i in range(self.size[0])}
        self.walls |= {(i, 0) for i in range(self.size[1])}
        self.walls |= {(self.size[1], i) for i in range(self.size[0])}
        self.walls |= {(i, self.size[0]) for i in range(self.size[1])}

    def print(self):
        txt = ""
        for row in self._data:
            for el in row:
                txt += colored(
                    f"{el} ",
                    foreground=Color.BLACK if not el else Color.BRIGHT_WHITE,
                    background=Color.BLACK if not el else Color.BRIGHT_WHITE,
                )
            txt += "\n"
        print(txt)

    def generate(self) -> list[list[int]]:
        pos = (random.randint(2, self.size[1] - 2), random.randint(2, self.size[0] - 2))
        _Cursor(self, pos).draw()
        self._merge_zones()
        return self._data

    def _merge_zones(self):
        all_fields: set[Vector2] = set()
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if not self[i, j]:
                    all_fields.add((i, j))
        walls = self.get_zones_walls(all_fields, set(), set())
        if len(walls) == 1:
            return
        if len(walls) == 2:
            self[random.choice(list(walls[0] & walls[1]))] = 0
            return
        i = 1
        while len(walls) > 1:
            current_zone = walls[0]
            zone = walls[i]
            union = current_zone & zone
            if len(union) > 0:
                self[wall := random.choice(list(union))] = 0
                walls[0] |= zone
                walls[0].discard(wall)
                walls.pop(i)
                i = 0
            i += 1

    def get_zones_walls(
        self, fields: set[Vector2], scanned: set[Vector2], walls: set[Vector2]
    ) -> list[set[Vector2]]:
        if len(fields) == 0:
            return []
        _ZoneField(self, fields.copy().pop()).get_zone(scanned, walls)
        scanned2, walls2 = set(), set()
        zones = self.get_zones_walls(fields - scanned, scanned2, walls2)
        return [walls] + zones

    def get_available_positions(self, pos: Vector2) -> list[Vector2]:
        return [
            pos
            for pos in self.get_positions(pos)
            if pos not in self.walls and not self[pos]
        ]

    def get_walls(self, pos: Vector2) -> list[Vector2]:
        return [
            wall for wall in self.get_positions(pos) if wall in self.walls or self[wall]
        ]

    def is_edge(self, pos: Vector2) -> bool:
        return (
            pos[0] == 0
            or pos[1] == 0
            or pos[1] == self.size[0]
            or pos[0] == self.size[1]
        )

    def get_positions(self, pos: Vector2) -> list[Vector2]:
        ls = [
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
        ]
        for el in ls:
            if (
                el[0] <= 0
                or el[1] <= 0
                or el[1] >= self.size[0] - 1
                or el[0] >= self.size[1] - 1
            ):
                ls.remove(el)
        return ls

    def __setitem__(self, key: Vector2, value: int):
        self._data[key[0]][key[1]] = value

    def __getitem__(self, key: Vector2) -> int:
        return self._data[key[0]][key[1]]


class _Cursor:
    def __init__(self, world: World, pos: Vector2):
        self.world = world
        self.pos = pos

    def draw(self):
        self.world.walls.add(self.pos)
        self.world[self.pos] = 0
        positions = self.world.get_available_positions(self.pos)
        if len(positions) == 0:
            return
        if len(positions) == 1:
            _Cursor(self.world, positions[0]).draw()
            return
        walls = random_amount(positions, len(positions) - 1)
        for wall in walls:
            self.world[wall] = 1
            positions.remove(wall)
        for pos in positions:
            if not self.world[pos]:
                _Cursor(self.world, pos).draw()


class _ZoneField:
    def __init__(self, world: World, pos: Vector2):
        self.world = world
        self.pos = pos

    def get_zone(self, scanned: set[Vector2], walls: set[Vector2]):
        scanned.add(self.pos)
        positions = self.world.get_positions(self.pos)
        for pos in positions:
            is_wall = self.world[pos]
            if is_wall and pos not in walls:
                walls.add(pos)
            elif not is_wall and pos not in scanned:
                _ZoneField(self.world, pos).get_zone(scanned, walls)


sz: tuple[int, int] = tuple(map(int, sys.argv[1].split("x", maxsplit=1)))  # type: ignore
init_start = time.time()
wrld = World(sz)
gen_start = time.time()
wrld.generate()
print_start = time.time()
wrld.print()
end = time.time()
print(
    f"World init: \t{init_start - gen_start}s\n"
    f"World gen: \t{print_start - gen_start}s\n"
    f"Print: \t\t{end - print_start}s\n"
    f"Total: \t\t{end - init_start}s"
)
