#!/usr/bin/env python3
""" 2. Measure the runtime """
import asyncio
from time import perf_counter
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ measure_time: takes in two int arguments (in this order):
     n and max_delay. You will spawn wait_n(n, max_delay)
      with the specified arguments
    """
    start_time = perf_counter()
    asyncio.run(wait_n(n, max_delay))

    end_time = perf_counter()
    return (end_time - start_time) / n