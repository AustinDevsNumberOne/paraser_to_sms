import os

import asyncio
import mimetypes

from nudenet import NudeClassifier


PATH_TO_SAVE = "./output"


async def move_nsfw(file):
    try:
        os.rename(file, f"{PATH_TO_SAVE}/nsfw/{file.rsplit('/')[-1]}")
    except FileExistsError:
        ...


async def sort():

    loop = asyncio.get_event_loop()
    detector = await loop.run_in_executor(None, NudeClassifier)

    for file in os.listdir(PATH_TO_SAVE):
        file = f"{PATH_TO_SAVE}/{file}"

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

asyncio.run(sort())
