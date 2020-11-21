import os
import math
import asyncio
import mimetypes

import aiohttp
import aiofiles
from nudenet import NudeClassifier


BASE_URL = "http://gs.3g.cn/D/{}/w"

PROBABLY_MAX_RANGE = 0xffffff
PATH_TO_SAVE = "./output"


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
                        async with aiofiles.open(f"E:/output/{file_n}.{file_type}", "wb+") as output:
                            await output.write(await response.read())
                            await asyncio.sleep(0.3)


async def move_nsfw(file):
    try:
        os.rename(file, f"{PATH_TO_SAVE}/nsfw/{file.rsplit('/')[-1]}")
    except FileExistsError:
        ...


async def nude_sort():
    loop = asyncio.get_event_loop()
    detector = await loop.run_in_executor(None, NudeClassifier)
    already_checked = []
    while True:
        for file in os.listdir(PATH_TO_SAVE):
            file = f"{PATH_TO_SAVE}/{file}"
            if file in already_checked:
                continue
    
            already_checked.append(file)
            if os.path.isfile(file) and not os.path.isdir(file):
                mime_type = mimetypes.guess_type(file)[0].split("/")[0]
                try:
                    score = 0
                    if mime_type == "video":
                        result = await loop.run_in_executor(None, detector.classify_video, file)
                        frames = 0
                        for pred in result.get("metadata", {}).get("preds", {}).values():
                            score += pred.get("unsafe", 0)
                            frames += 1
                        if frames:
                            score /= frames

                    elif mime_type == "image":
                        result = await loop.run_in_executor(None, detector.classify, file)
                        score = result.get(file, {}).get("unsafe", 0)

                    if score and score >= 0.8:
                        await move_nsfw(file)
                except LookupError:
                    ...
        await asyncio.sleep(30)


async def main():
    number_of_getters = 10
    ranges = math.ceil(PROBABLY_MAX_RANGE // 10)
    futures = []
    for i in range(number_of_getters):
        in_range = range(ranges * i, ranges * (i + 1))
        futures.append(asyncio.ensure_future(async_get(in_range)))

    futures.append(asyncio.ensure_future(nude_sort()))
    for future in futures:
        await future

try:
    os.makedirs(f"{PATH_TO_SAVE}/nsfw")
except FileExistsError:
    ...

asyncio.run(main())
