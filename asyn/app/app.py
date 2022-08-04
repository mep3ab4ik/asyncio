import asyncio
from time import time

from aiohttp import web, request
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from asyn.part1.sites import sites


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 ' \
             'Safari/537.36 OPR/86.0.4363.64 '

site_check_results = {}


async def background_task(app):
    while True:

        pending = [send_request(site) for site in sites]

        while pending:
            done, pending = await asyncio.wait(pending, timeout=1, return_when=asyncio.FIRST_COMPLETED)
            task_result = done.pop().result()

            url, status = task_result

            site_check_results[url] = {
                'status': status,
                'time': time()
            }

        print(time(), 'Background task completed successfully')
        await asyncio.sleep(10)


async def start_background_tasks(app):
    app['background_task'] = asyncio.create_task(background_task(app))


async def stop_background_tasks(app):
    app['background_task'].cancel()
    await app['background_task']


async def send_request(url):
    async with request('GET', url, headers={'User-Agent': user_agent}) as response:
        return url, response.status


async def ping(request:Request):
    return site_check_results


async def health(request:Request):
    return {'message': 'ok'}


@middleware
async def json_middleware(request, handler):
    resp = await handler(request)
    return json_response(resp)

app = web.Application(middlewares=[json_middleware])
app.router.add_route('GET', '/ping', ping)
app.router.add_route('GET', '/health', health)
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(stop_background_tasks)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1')
