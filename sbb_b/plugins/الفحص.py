import random
import re
import time
from datetime import datetime
from platform import python_version

import requests
from telethon import version, Button, events
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery
from sbb_b import StartTime, olgaversion, sbb_b

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import check_data_base_heal_th, get_readable_time, olgaalive
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention


@sbb_b.ar_cmd(pattern="فحص$")
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    ANIME = None
    olga_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    if "ANIME" in olga_caption:
        data = requests.get("https://animechan.vercel.app/api/random").json()
        ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    olgaevent = await edit_or_reply(event, "**᯽︙ يتـم التـأكـد انتـظر قليلا رجاءً**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "⿻┊‌‎"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**[ 𝐒𝗈𝐮𝐫𝐜𝐞 𝐎𝐥𝐆𝐀 ](t.me/B_F49)**"
    olga_IMG = gvarstatus("ALIVE_PIC")
    caption = olga_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        ANIME=ANIME,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        tepver=olgaversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if olga_IMG:
        olga = list(olga_IMG.split())
        PIC = random.choice(olga)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await olgaevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                olgaevent,
                f"**رابط الصورة غير صحيح**\nعليك الرد على رابط الصورة ب .اضف صورة الفحص",
            )
    else:
        await edit_or_reply(
            olgaevent,
            caption,
        )


temp = """{ALIVE_TEXT}
**⌗ ┊ {EMOJI}‌‎‌‎𝙽𝙰𝙼𝙴 𖤐 {mention}** ٫
**⌗ ┊ {EMOJI}‌‎‌‎𝙿𝚈𝚃𝙷𝙾𝙽 𖤐 {pyver}** ٫
**⌗ ┊ {EMOJI}‌‎‌‎𝘣id𝖀 𖤐 𖠄 {telever}** ٫
**⌗ ┊ {EMOJI}‌‌‎‌‎𝚄𝙿𝚃𝙸𝙼𝙴 {uptime}** ٫
**⌗ ┊ {EMOJI} ‌‎‌‎‌‎𝙿𝙸𝙽𝙶 {ping}** ٫
**𖠄 𝘣id𝖀 𝘂𝘀𝗲𝗿𝗯𝗼𝘁 𖤐**"""


def olgaalive_text():
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    olga_caption = "『  𝘣id𝖀 𝙸𝚂 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 ✓  』*\n"
    olga_caption += f"**{EMOJI} اصدار التيليثون :** `{version.__version__}\n`"
    olga_caption += f"**{EMOJI} اصدار أولكَا :** `{olgaversion}`\n"
    olga_caption += f"**{EMOJI} اصدار البايثون :** `{python_version()}\n`"
    olga_caption += f"**{EMOJI} المالك:** {mention}\n"
    return olga_caption


@sbb_b.ar_cmd(pattern="السورس$")
async def repo(event):
    RR7PP = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await sbb_b.inline_query(f444or, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()

ROZ_PIC = "https://telegra.ph/file/205ec41e8f36243634e44.png"
RAZAN = Config.TG_BOT_USERNAME
ROZ_T = (
    f"**⌯︙بوت أولكَا يعمل بنجاح 🤍،**\n"
    f"**   - اصدار التليثون :** `1.23.0\n`"
    f"**   - اصدار أولكَا :** `4.0.0`\n"
    f"**   - البوت المستخدم :** `{RAZAN}`\n"
    f"**   - اصدار البايثون :** `3.9.6\n`"
    f"**   - المستخدم :** {mention}\n"
)

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await sbb_b.get_me()
        if query.startswith("السورس") and event.query.user_id == sbb_b.uid:
            buttons = [
                [
                    Button.url("قنـاة السـورس ⚙️", "https://t.me/B_F49"),
                    Button.url("المطـور 👨🏼‍💻", "https://t.me/f444or"),
                ]
            ]
            if ROZ_PIC and ROZ_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    ROZ_PIC, text=ROZ_T, buttons=buttons, link_preview=False
                )
            elif ROZ_PIC:
                result = builder.document(
                    ROZ_PIC,
                    title="bidu - USERBOT",
                    text=ROZ_T,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="bidu - USERBOT",
                    text=ROZ_T,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)




# edit by ~ @f444or
