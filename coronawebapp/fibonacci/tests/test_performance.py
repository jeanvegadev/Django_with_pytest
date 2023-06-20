from fibonacci.fibonacci_dinamico import fibonacci_dynamic
import pytest
from fixtures import track_performance
from time import sleep


@pytest.mark.performance
@track_performance
def test_performance():
    sleep(3)
    fibonacci_dynamic(1000)




