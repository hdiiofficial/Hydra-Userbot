import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time
from config import CMD_HANDLER as cmd
from pyrogram import filters
from pyrogram.types import Message
from ProjectMan.helpers.basic import edit_or_reply

from .help import add_command_help

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message(filters.command("eval", cmd) & filters.me)
async def executor(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="__Nigga Give me some command to execute.__"
        )
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**OUTPUT**:\n```{evaluation.strip()}```"
    await edit_or_reply(message, final_output)
#    if len(final_output) > 4096:
#        filename = "output.txt"
#        with open(filename, "w+", encoding="utf8") as out_file:
#            out_file.write(str(evaluation.strip()))
#        t2 = time()
#        await message.reply_document(
#            document=filename,
#            caption=f"**INPUT:**\n`{cmd[0:980]}`\n\n**OUTPUT:**\n`Attached Document`",
#            quote=False
#        )
#        await message.delete()
#        os.remove(filename)
#    else:
#        t2 = time()
#        await edit_or_reply(
#            message, text=final_output
#        )
