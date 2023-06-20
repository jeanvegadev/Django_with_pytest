from typing import Callable
from datetime import timedelta, datetime


class PerformanceException(Exception):
    def __init__(self, runtime: timedelta, limit:timedelta) -> None:
        self.runtime = runtime
        self.limit = limit
        
    def __str__(self) -> str:
        return "Performance test failed,"\
               f" runtime = {self.runtime.total_seconds()},"\
               f" limit: {self.limit.total_seconds()}"

def track_performance(method:Callable, runtime_limit=timedelta(seconds=2)):
    def run_function_and_validate_runtime(*args,**kw):
        tik = datetime.now()
        result = method(*args,**kw)
        tok= datetime.now()
        runtime = tok - tik
        print(f"\n runtime: {runtime.total_seconds()}")

        if runtime > runtime_limit:
            raise PerformanceException(runtime= runtime, limit=runtime_limit)
        return result

    return run_function_and_validate_runtime