import requests
from telethon.tl import functions

from .. import sbb_b
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..utils.tools import create_supergroup
from sbb_b.sql_helper.globals import gvarstatus
ansh = gvarstatus("ANT7AL") or "(الانشاء|الإنشاء|انشاء الحساب|انشائي)"

headers = {
    'Host': 'restore-access.indream.app',
    'Connection': 'keep-alive',
    'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
    'Accept': '*/*',
    'Accept-Language': 'ar',
    'Content-Length': '25',
    'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}

@sbb_b.ar_cmd(pattern="صنع (مجموعة خارقة|مجموعة عادية|قناة) ([\s\S]*)")
async def _(event):
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "قناة":
        descript = "تم صنع هذه القناة بواسطة سورس أولكَا"
    else:
        descript = "تم صنع المجموعة باستخدام سورس أولكَا"
    if type_of_group == "مجموعة عادية":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"**- المجموعة `{group_name}` تم بنجاح صنعها {result.link}**"
            )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n{str(e)}")
    elif type_of_group == "قناة":
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )
            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"**- القناة {group_name} تم بنجاح صنعها {result.link}**"
            )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n{e}")
    elif type_of_group == "مجموعة خارقة":
        answer = await create_supergroup(
            group_name, event.client, Config.TG_BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await edit_or_reply(
                event,
                f"تم صنع المجموعة `{group_name}` بنجاح الرابط الرابط: {answer[0].link}",
            )
        else:
            await edit_delete(event, f"**خطأ:**\n{answer[1]}")
    else:
        await edit_delete(event, "استخدم الامر بشكل صحيح")

@sbb_b.ar_cmd(pattern=f"{ansh}$")
async def t7(event):
    headers = {
        'Content-Type': 'application/json'
    }
    data = '{"telegramId":' + str(event.text) + '}'
    response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
    date = response.get('data', {}).get('date', None)
    if date:
        mej = f"~ الايدي {event.text}\n ~ تاريخ انشاء الحساب {date}"
        await event.client.send_message(event.message, mej)
