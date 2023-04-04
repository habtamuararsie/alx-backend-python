#!/usr/bin/env python3
"""
Measure the runtime
"""

import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    return the total runtime and calculate the time
    """
    start = time.perf_counter()
    tasks = [async_comprehension() for i in range(4)]
    await asyncio.gather(*tasks)
    end = time.perf_counter()
    return end - start
