# ExenWorldGen
Module for quicks maze-like 2D world generations <br>
![https://github.com/Exenifix/worldgen/blob/master.github/res/maze.png](https://github.com/Exenifix/worldgen/blob/master/.github/res/maze.png?raw=1)

## Installation
Library is available on PyPI:
```shell
$ pip install exenworldgen
```

## Code Usage
```python
from exenworldgen import World

world = World((25, 25))
data = world.generate()  # data can also be obtained via world.data
world.print()  # print the world
```

## CLI Usage
```shell
python -m exenworldgen 25x25      # one world of size 25x25
python -m exenworldgen 10x10 30   # 30 worlds of size 10x10
```
