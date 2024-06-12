import os

from PIL import Image

from sbb_b.core.logger import logging
from sbb_b.core.managers import edit_or_reply
from sbb_b.helpers.functions.vidtools import take_screen_shot
from sbb_b.helpers.tools import fileinfo, media_type, meme_type
from sbb_b.helpers.utils.utils import runcmd

LOGS = logging.getLogger(__name__)


class olgaConverter:
    async def _media_check(self, reply, dirct, file, memetype):
        if not os.path.isdir(dirct):
            os.mkdir(dirct)
        olgafile = os.path.join(dirct, file)
        if os.path.exists(olgafile):
            os.remove(olgafile)
        try:
            olgamedia = reply if os.path.exists(reply) else None
        except TypeError:
            if memetype in ["Video", "Gif"]:
                dirct = "./temp/olgafile.mp4"
            elif memetype == "Audio":
                dirct = "./temp/olgafile.mp3"
            olgamedia = await reply.download_media(dirct)
        return olgafile, olgamedia

    async def to_image(
        self, event, reply, dirct="./temp", file="meme.png", noedits=False, rgb=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype == "Document":
            return event, None
        olgaevent = (
            event
            if noedits
            else await edit_or_reply(event, "- جار التحويل يرجى الانتظار")
        )
        olgafile, olgamedia = await self._media_check(reply, dirct, file, memetype)
        if memetype == "Photo":
            im = Image.open(olgamedia)
            im.save(olgafile)
        elif memetype in ["Audio", "Voice"]:
            await runcmd(f"ffmpeg -i '{olgamedia}' -an -c:v copy '{olgafile}' -y")
        elif memetype in ["Round Video", "Video", "Gif"]:
            await take_screen_shot(olgamedia, "00.00", olgafile)
        if mediatype == "Sticker":
            if memetype == "Animated Sticker":
                olgacmd = f"lottie_convert.py --frame 0 -if lottie -of png '{olgamedia}' '{olgafile}'"
                stdout, stderr = (await runcmd(olgacmd))[:2]
                if stderr:
                    LOGS.info(stdout + stderr)
            elif memetype == "Video Sticker":
                await take_screen_shot(olgamedia, "00.00", olgafile)
            elif memetype == "Static Sticker":
                im = Image.open(olgamedia)
                im.save(olgafile)
        if olgamedia and os.path.exists(olgamedia):
            os.remove(olgamedia)
        if os.path.exists(olgafile):
            if rgb:
                img = Image.open(olgafile)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(olgafile)
            return olgaevent, olgafile, mediatype
        return olgaevent, None

    async def to_sticker(
        self, event, reply, dirct="./temp", file="meme.webp", noedits=False, rgb=False
    ):
        filename = os.path.join(dirct, file)
        response = await self.to_image(event, reply, noedits=noedits, rgb=rgb)
        if response[1]:
            image = Image.open(response[1])
            image.save(filename, "webp")
            os.remove(response[1])
            return response[0], filename, response[2]
        return response[0], None

    async def to_webm(
        self, event, reply, dirct="./temp", file="animate.webm", noedits=False
    ):
        memetype = await meme_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Gif",
            "Video",
        ]:
            return event, None
        olgaevent = (
            event
            if noedits
            else await edit_or_reply(event, "- يتم التحويل الى ملصق متحرك")
        )
        olgafile, olgamedia = await self._media_check(reply, dirct, file, memetype)
        media = await fileinfo(olgamedia)
        h = media["height"]
        w = media["width"]
        w, h = (-1, 512) if h > w else (512, -1)
        await runcmd(
            f"ffmpeg -to 00:00:02.900 -i '{olgamedia}' -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an '{olgafile}'"
        )  # pain
        if os.path.exists(olgamedia):
            os.remove(olgamedia)
        if os.path.exists(olgafile):
            return olgaevent, olgafile
        return olgaevent, None

    async def to_gif(
        self, event, reply, dirct="./temp", file="meme.mp4", maxsize="5M", noedits=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Animated Sticker",
            "Video",
            "Gif",
        ]:
            return event, None
        olgaevent = (
            event
            if noedits
            else await edit_or_reply(event, "- جار التحويل يرجى الانتظار")
        )
        olgafile, olgamedia = await self._media_check(reply, dirct, file, memetype)
        if mediatype == "Sticker":
            if memetype == "Video Sticker":
                await runcmd(f"ffmpeg -i '{olgamedia}' -c copy '{olgafile}'")
            elif memetype == "Animated Sticker":
                await runcmd(f"lottie_convert.py '{olgamedia}' '{olgafile}'")
        if olgamedia.endswith(".gif"):
            await runcmd(
                f"ffmpeg -f gif -i '{olgamedia}' -fs {maxsize} -an '{olgafile}'"
            )
        else:
            await runcmd(
                f"ffmpeg -i '{olgamedia}' -c:v libx264 -fs {maxsize} -an '{olgafile}'"
            )
        if olgamedia and os.path.exists(olgamedia):
            os.remove(olgamedia)
        if os.path.exists(olgafile):
            return olgaevent, olgafile
        return olgaevent, None


Convert = olgaConverter()
