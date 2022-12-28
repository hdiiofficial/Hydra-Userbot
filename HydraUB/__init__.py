import asyncio
import logging
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client
from pytgcalls import GroupCallFactory
from config import (
    API_HASH,
    API_ID,
    UBOT_LOG,
    DB_URL,
    STRING_SESSION,
    STRING_SESSION1,
    STRING_SESSION2,
    STRING_SESSION3,
    STRING_SESSION4,
    SUDO_USERS,
)

# LOGGER
LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

LOGS = logging.getLogger(__name__)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# setting

if (
    not STRING_SESSION
    and not STRING_SESSION1
    and not STRING_SESSION2
    and not STRING_SESSION3
    and not STRING_SESSION4
):
    LOGGER(__name__).error("No String Session Found! Exiting!")
    sys.exit()

if not API_ID:
    LOGGER(__name__).error("No API_ID Found! Exiting!")
    sys.exit()

if not API_HASH:
    LOGGER(__name__).error("No API_HASH Found! Exiting!")
    sys.exit()

if UBOT_LOG:
    UBOT_LOG = UBOT_LOG
else:
    UBOT_LOG = "me"

LOOP = asyncio.get_event_loop()

trl = Translator()

aiosession = ClientSession()

CMD_HELP = {}

scheduler = AsyncIOScheduler()

StartTime = time.time()


# connection to pyrogram 

ubot1 = (
    Client(
        name="ubot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION,
        plugins=dict(root="Hydra-UB/plugins"),
    )
    if STRING_SESSION
    else None
)

ubot2 = (
    Client(
        name="ubot2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION1,
        plugins=dict(root="Hydra-UB/plugins"),
    )
    if STRING_SESSION1
    else None
)

ubot3 = (
    Client(
        name="ubot3",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION2,
        plugins=dict(root="Hydra-UB/plugins"),
    )
    if STRING_SESSION2
    else None
)

ubot4 = (
    Client(
        name="ubot4",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION3,
        plugins=dict(root="Hydra-UB/plugins"),
    )
    if STRING_SESSION3
    else None
)

ubot5 = (
    Client(
        name="ubot5",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=STRING_SESSION4,
        plugins=dict(root="Hydra-UB/plugins"),
    )
    if STRING_SESSION4
    else None
)

ubots = [ubot for ubot in [ubot1, ubot2, ubot3, ubot4, ubot5] if ubot]

for ubot in ubots:
    if not hasattr(ubot, "group_call"):
        setattr(ubot, "group_call", GroupCallFactory(ubot).get_group_call())


# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
# Clone by hdiiofficial :v
