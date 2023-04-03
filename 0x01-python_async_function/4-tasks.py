#!/usr/bin/env python3
""" 1. Let's execute multiple coroutines at the same time with async"""

import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
        wait_n: takes in 2 int arguments
        (in this order): n and max_delay.
        """
    tasks = (task_wait_random(max_delay) for i in range(n))
    lst = await asyncio.gather(*tasks)
    return sorted(lst)