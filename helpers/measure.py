import time
from functools import wraps
from typing import Callable


def measure(func: Callable) -> Callable:
    """Measure the execution time of a function.
    Usage:
        `@measure` decorator in front of function to be measured.

    Args:
        func (Callable): The function to measure.

    Returns:
        Callable: The wrapped measurement function.
    """

    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time.time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time.time() * 1000)) - start
            print(
                f"Total execution time for {func.__name__}: {end_ if end_ > 0 else 0} ms"
            )

    return _time_it


@measure
def add(a, b):
    """Example function to demonstrate @measure"""
    return a + b


if __name__ == "__main__":
    print(add(1, 2))
