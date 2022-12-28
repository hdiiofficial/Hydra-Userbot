import asyncio
import shlex
import socket
from typing import Tuple

import dotenv
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from config import HEROKU_API_KEY, HEROKU_APP_NAME
from HydraUB import LOGGER

HAPP = None


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())



def is_heroku():
    return "heroku" in socket.getfqdn()


def heroku():
    global HAPP
    if is_heroku:
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                LOGGER("Hydra-UB").info(f"Heroku App Configured")
            except BaseException as e:
                LOGGER("Heroku").error(e)
                LOGGER("Heroku").info(
                    f"see HEROKU_API_KEY and HEROKU_APP_NAME on heroku vars and true"
                )


async def in_heroku():
    return "heroku" in socket.getfqdn()


async def create_botlog(client):
    if HAPP is None:
        return
    LOGGER("Hydra-UB").info(
        "Waiittt. CREATING YOUR GROUP LOG USERBOT"
    )
    desc = "Group Log for Hydra-UserBot.\n\nPlease don't leave.\n\n✨ Powered By ~ @hdiiofficial ✨"
    try:
        gruplog = await ubot.create_supergroup("Log UserBot", desc)
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["UBOT_LOG"] = gruplog.id
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "UBOT_LOG", gruplog.id)
    except Exception:
        LOGGER("Hydra-UB").warning(
            "Cant find UBOT_LOG"
        )


#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
