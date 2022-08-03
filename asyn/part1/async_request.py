import asyncio
from time import time

import aiohttp

from .sites import sites

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 ' \
             'Safari/537.36 OPR/86.0.4363.64 '


async def send_request(url):
    start_time = time()

    async with aiohttp.request('GET', url,headers={'User-Agent': user_agent}) as response:
        await response.text()
        print(f'[{url}] Time elapsed: {time() - start_time:.2f}s. ({response.status})')


async def main():
    start_time = time()
    tasks = [send_request(site) for site in sites]
    await asyncio.gather(*tasks)

    print(f'Total time: {time() - start_time:.2f}s')


if __name__ == '__main__':
    asyncio.run(main())
