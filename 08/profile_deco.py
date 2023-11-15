import cProfile
import io
import pstats
from typing import Any

def profile_deco(func):
    class Wraper:
        def __init__(self) -> None:
            self.profiler = cProfile.Profile()
 
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            self.profiler.enable()
            res = func(*args, **kwargs)
            self.profiler.disable()
            return res

        def print_stat(self) -> None:
            output = io.StringIO()
            stats = pstats.Stats(self.profiler, stream=output)
            stats.print_stats()
            print(output.getvalue())

    return Wraper()


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


if __name__ == "__main__":
    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()