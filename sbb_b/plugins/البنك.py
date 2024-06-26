import os
from datetime import datetime

from sbb_b import sbb_b

#
from . import hmention, reply_id

PING_PIC = os.environ.get("PING_PIC") or (
    "hhttps://telegra.ph/file/8b3a73ecb73e6b2afd034.jpg"
)

JM_TXT = os.environ.get("PING_TEXT") or "- أصلًا عادِي عمرها مَ كانت عادِي ."


@sbb_b.ar_cmd(pattern="بنك$")
async def _(event):
    reply_to_id = await reply_id(event)
    start = datetime.now()
    roz = await edit_or_reply(
        event, "<b><i> البــــنك...</b></i>", "html"
    )
    end = datetime.now()
    await roz.delete()
    ms = (end - start).microseconds / 1000
    if PING_PIC:
        caption = f"<b><i>{JM_TXT}<i><b>\n<code>┏━━━━━━━┓\n┃ ✦ {ms}\n┃ ✦ <b>{hmention}</b>\n┗━━━━━━━┛"
        await event.client.send_file(
            event.chat_id,
            PING_PIC,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to_id,
            link_preview=False,
            allow_cache=True,
        )
    else:
        await event.edit_or_reply(
            event, "<code>يجـب اضـافة متـغير `PING_PIC`  اولا  f<code>", "html"
        )

