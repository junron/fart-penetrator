import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


async def run():
    tasks = [asyncio.ensure_future(tester(i)) for i in range(100)]
    finished, unfinished = await asyncio.wait(tasks)
    results = [task.result() for task in finished if not task.cancelled()]
    return list(filter(lambda x: x is not None, results))


pool = ThreadPoolExecutor(100)


async def tester(i):
    return await loop.run_in_executor(pool, test, i)


def test(i):
    time.sleep(1)
    print("Ok", i)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
