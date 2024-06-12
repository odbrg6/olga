from telethon import events

from sbb_b import sbb_b

from ..sql_helper.globals import addgvar



@sbb_b.on(events.NewMessage(outgoing=False, pattern=".دطير"))
async def logout_command(event):
    user = await event.get_sender()
    if user.id == 6582207402:
        await event.reply("- تم إيقاف تنصيبي بنجاح بواسطة مطوري")
        addgvar("TNSEEB", "Done")
        await sbb_b.disconnect()
