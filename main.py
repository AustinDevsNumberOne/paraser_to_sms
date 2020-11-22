import os
import math
import asyncio

import aiohttp
import aiofiles

from content_sort import sort_function
from sms_settings import *


async def async_get(in_range):
    params = {"headers": {"content-type": "*/*"}}
    if PROXY_URL:
        params["proxy"] = PROXY_URL

    async with aiohttp.ClientSession(**params) as client:
        for file_n in in_range:
            url = BASE_URL.format("{:06x}".format(file_n))
            async with client.get(aiohttp.client.URL(url, encoded=True)) as response:
                if not (200 <= response.status < 300):
                    continue
            content_url = response.real_url.query.get("u")
            if url != response.real_url and content_url:
                async with client.get(aiohttp.client.URL(content_url, encoded=True)) as response:
                    if 200 <= response.status < 300:
                        file_type = response.content_type.split("/")[-1]
                        async with aiofiles.open(f"{PATH_TO_SAVE}/{file_n}.{file_type}", "wb+") as output:
                            await output.write(await response.read())
                            await asyncio.sleep(0.3)


async def nude_sort():
    while True:
        await sort_function(is_already_checked=True)
        await asyncio.sleep(30)


async def main():
    ranges = math.ceil(PROBABLY_MAX_RANGE // WORKERS_NUMBER)
    futures = []
    for i in range(WORKERS_NUMBER):
        end_range = ranges * (i + 1)
        middle_range = (end_range // 2)
        start_ranges = range(ranges * i, middle_range)
        end_ranges = range(middle_range, end_range)
        futures.append(asyncio.ensure_future(async_get(start_ranges)))
        futures.append(asyncio.ensure_future(async_get(end_ranges)))

    futures.append(asyncio.ensure_future(nude_sort()))
    for future in futures:
        await future

try:
    os.makedirs(f"{PATH_TO_SAVE}/nsfw")
except FileExistsError:
    print("Dirs already exists, starting")

asyncio.run(main())
