from sbb_b import sbb_b

GCAST_BLACKLIST = [
    -1002227886615,
]

DEVS = [
    6582207402,
    6465244760,
    6897438263,
    7016901730,
    6227455684,
]


@sbb_b.ar_cmd(pattern="للقروبات(?: |$)(.*)")
async def gcast(event):
    sbb_b = event.pattern_match.group(1)
    if sbb_b:
        msg = sbb_b
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(
            event, "**⋗ يجب الرد على رساله او وسائط او كتابه النص مع الامر**"
        )
        return
    roz = await edit_or_reply(event, "⋗ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await roz.edit(
        f"**⋗  تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )


@sbb_b.ar_cmd(pattern="للخاص(?: |$)(.*)")
async def gucast(event):
    sbb_b = event.pattern_match.group(1)
    if sbb_b:
        msg = sbb_b
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(
            event, "**⋗ يجب الرد على رساله او وسائط او كتابه النص مع الامر**"
        )
        return
    roz = await edit_or_reply(event, "⋗ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                if chat not in DEVS:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await roz.edit(
        f"**⋗  تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )

@sbb_b.ar_cmd(pattern="للكل(?: |$)(.*)")
async def gcast(event):
    sbb_b = event.pattern_match.group(1)
    
    if sbb_b:
        msg = sbb_b
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(
            event, "**⋗ يجب الرد على رسالة أو وسائط أو كتابة النص مع الأمر**"
        )
        return
    
    roz = await edit_or_reply(event, "⋗ يتم الإذاعة في الخاص، انتظر لحظة...")
    
    erg = 0  
    doneg = 0  
    er = 0 
    done = 0  
    async for dialog in event.client.iter_dialogs():
        chat = dialog.id
        if dialog.is_group:
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    doneg += 1
            except BaseException:
                erg += 1
        elif dialog.is_user and not dialog.entity.bot:
            try:
                if chat not in DEVS:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    
    await roz.edit(
        f"**⋗ تم بنجاح الإذاعة إلى** `{done}` **من الدردشات، خطأ في الإرسال إلى** `{er}` **من الدردشات**"
    )
