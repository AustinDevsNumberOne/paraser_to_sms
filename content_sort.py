import os

import asyncio
import mimetypes
import math
from nudenet import NudeClassifier
from sms_settings import *

already_checked = []


async def move_nsfw(file):
    try:
        os.rename(file, f"{PATH_TO_SAVE}/nsfw/{file.rsplit('/')[-1]}")
    except FileExistsError:
        print(f"File {file} already in nswf")


async def sort_algorithm(files, loop, detector, is_already_checked):
    global already_checked
    for file in files:
        file = f"{PATH_TO_SAVE}/{file}"
        if file in already_checked and is_already_checked:
            continue

        is_already_checked and already_checked.append(file)
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

                if score and score >= NSFW_SENSITIVE:
                    await move_nsfw(file)
            except LookupError:
                print(f"Can`t identify image/video {file} content by neuron network.")


async def sort_function(is_already_checked=True):

    loop = asyncio.get_event_loop()
    detector = await loop.run_in_executor(None, NudeClassifier)

    all_files = os.listdir(PATH_TO_SAVE)
    all_files_len = len(all_files)
    middle_index = math.ceil(all_files_len/2)
    await sort_algorithm(all_files[:middle_index], loop, detector, is_already_checked)
    await sort_algorithm(all_files[middle_index:], loop, detector, is_already_checked)

try:
    os.makedirs(f"{PATH_TO_SAVE}/nsfw")
except FileExistsError:
    print("Dirs already exists")

asyncio.run(sort_function(is_already_checked=False))
