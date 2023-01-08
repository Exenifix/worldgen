import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def random_amount(population: Sequence[T], maxk: int) -> list[T]:
    k = random.randint(0, maxk)
    if k == 0:
        return []
    return random.sample(population, k=k)
