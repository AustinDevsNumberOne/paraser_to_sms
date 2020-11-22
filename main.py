import os
import math
import asyncio
from functools import partial

import cv2
import numpy
import aiohttp
import aiofiles
from skimage.metrics import structural_similarity

from content_sort import sort_function
from sms_settings import *


IS_IGNORED_UPLOADED = asyncio.Event()
IS_IGNORED_UPLOADED.clear()


async def update_ignored():
    path = f"{PATH_TO_SAVE}/ignored"
    while True:
        IS_IGNORED_UPLOADED.clear()
        for file in os.listdir(path):
            file = f"{path}/{file}"
            async with aiofiles.open(file, "rb") as ignored_file:
                ignored_bytes = await ignored_file.read()
                if ignored_bytes not in ignored:
                    np_res = numpy.frombuffer(ignored_bytes, numpy.uint8)
                    ignored[ignored_bytes] = cv2.imdecode(np_res, cv2.COLOR_BGR2GRAY)
        IS_IGNORED_UPLOADED.set()
        await asyncio.sleep(5)


async def check_for_ignoring(img_bytes):
    loop = asyncio.get_event_loop()
    np_res = numpy.frombuffer(img_bytes, numpy.uint8)
    img = cv2.imdecode(np_res, cv2.COLOR_BGR2GRAY)
    if img is not None:
        await IS_IGNORED_UPLOADED.wait()
        for ignored_pic in ignored.values():
            height, weight, *_ = img.shape
            ignored_pic = cv2.resize(ignored_pic, (weight,height))

            part = partial(structural_similarity, im1=ignored_pic.astype(numpy.float32),
                           im2=img.astype(numpy.float32), multichannel=True)
            score = await loop.run_in_executor(None, part)
            if score >= 0.8:
                return True
    return False


async def async_get(in_range):
    params = {"headers": {"content-type": "*/*"}}
    if PROXY_URL:
        params["proxy"] = PROXY_URL

    async with aiohttp.ClientSession() as client:
        for file_n in in_range:
            url = BASE_URL.format("{:06x}".format(file_n))
            async with client.get(aiohttp.client.URL(url, encoded=True), **params) as response:
                if not (200 <= response.status < 300):
                    continue
            content_url = response.real_url.query.get("u")
            if url != response.real_url and content_url:
                async with client.get(aiohttp.client.URL(content_url, encoded=True), **params) as response:
                    if 200 <= response.status < 300:
                        mime_type, sub_type = response.content_type.split("/")
                        response_bytes = await response.read()
                        if mime_type == "image":
                            if await check_for_ignoring(response_bytes):
                                continue
                        async with aiofiles.open(f"{PATH_TO_SAVE}/{file_n}.{sub_type}", "wb+") as output:
                            response_bytes = await response.read()
                            await output.write(response_bytes)
                            await asyncio.sleep(0.3)


async def nude_sort():
    while True:
        await sort_function(is_already_checked=True)
        await asyncio.sleep(5)


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
    futures.append(asyncio.ensure_future(update_ignored()))
    for future in futures:
        await future

try:
    os.makedirs(f"{PATH_TO_SAVE}/nsfw")
    os.makedirs(f"{PATH_TO_SAVE}/ignored")
except FileExistsError:
    print("Dirs already exists, starting")

asyncio.run(main())
