import pytest
from typing import Callable
from fibonacci.fibonacci_dinamico import fibonacci_dynamic


@pytest.mark.parametrize("n, expected",
                         [(0,0), (1,1), (2,1), (3,2), (40,102334155)])
@pytest.mark.parametrize("fibo_func", [fibonacci_dynamic])
def test_fibonacci_dinamico(
        fibo_func: Callable[[int], int], n:int, expected:int)->None:
    res = fibonacci_dynamic(n)
    assert expected == res
    print(fibonacci_dynamic(n))
