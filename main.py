import os
import math
import asyncio

import aiohttp
import aiofiles


BASE_URL = "http://gs.3g.cn/D/{}/w"

PROBABLY_MAX_RANGE = 0xffffff


async def async_get(in_range):
    async with aiohttp.ClientSession(headers={"content-type": "*/*"}) as client:
        for file_n in in_range:
            url = BASE_URL.format("{:06x}".format(file_n))
            async with client.get(aiohttp.client.URL(url, encoded=True)) as response:
                if response.status not in range(200, 300):
                    continue
            content_url = response.real_url.query.get("u")
            if url != response.real_url and content_url:
                async with client.get(content_url) as response:
                    if response.status in range(200, 300):
                        file_type = response.content_type.split("/")[-1]
                        async with aiofiles.open(f"output/{file_n}.{file_type}", "wb+") as output:
                            await output.write(await response.read())
                            await asyncio.sleep(0.3)


async def main():
    number_of_getters = 10
    ranges = math.ceil(PROBABLY_MAX_RANGE // 10)
    futures = []
    for i in range(number_of_getters):
        in_range = range(ranges * i, ranges * (i + 1))
        futures.append(asyncio.ensure_future(async_get(in_range)))

    for future in futures:
        await future

if "output" not in os.listdir("."):
    os.mkdir("output")

asyncio.run(main())
