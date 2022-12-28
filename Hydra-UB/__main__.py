import importlib

from pyrogram import idle
from uvloop import install

from Hydra-UB import UBOT_LOG, LOGGER, LOOP, aiosession
from Hydra-UB import ubot1, ubots
from Hydra-UB.helpers.misc import create_botlog, heroku
from Hydra-UB.plugins import ALL_MODULES

BOT_VER = "main@0.0.1" 
CMD_HANDLER = "."

MSG_ON = """
🔥 **Hydra-Userbot Is Alive**
━━
➠ **Userbot Version -** `{}`
➠ **Ketik** `{}alive` **to check ur UBot**
━━
"""


async def main():
    for all_module in ALL_MODULES:
        importlib.import_module(f"Hydra-UB.plugins.{all_module}")
    for ubot in ubots:
        try:
            await ubot.start()
            ubot.me = await ubot.get_me()
            await ubot.join_chat("hdiiofficial")
            await ubot.join_chat("FutureCity005")
            try:
                await ubot.send_message(
                    UBOT_LOG, MSG_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("Hydra-UB").info(
                f"Logged in as {ubot.me.first_name} | [ {ubot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("Hydra-UB").info(f"Hydra-UserBot v{BOT_VER} [🔥 ACTIVED! 🔥]")
    if ubot1 and not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(ubot1)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Hydra-UB").info("Starting Hydra-UserBot")
    install()
    heroku()
    LOOP.run_until_complete(main())


# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
# Clone by hdiiofficial :v
