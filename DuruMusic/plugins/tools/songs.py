import os
import re
import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)

from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from strings import get_command
from DuruMusic import YouTube, app
from DuruMusic.utils.decorators.language import language, languageCB
from DuruMusic.utils.formatters import convert_bytes
from DuruMusic.utils.inline.song import song_markup

# Command
SONG_COMMAND = get_command("SONG_COMMAND")

@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def song_command_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SG_B_1"],
                    url=f"https://t.me/{app.username}?start=song",
                ),
            ]
        ]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)

@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@language
async def song_command_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)

    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])

        mystic = await message.reply_text(_["play_1"])
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)
        except Exception as e:
            return await mystic.edit_text(f"Error: {str(e)}")

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])

        mystic = await message.reply_text(_["play_1"])
        query = message.text.split(None, 1)[1]
        try:
            title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
        except Exception as e:
            return await mystic.edit_text(f"Error: {str(e)}")

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

# ... (rest of the code remains the same)

@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading...")
    except:
        pass

    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")

    mystic = await CallbackQuery.edit_message_text(_["song_8"])

    yturl = f"https://www.youtube.com/watch?v={vidid}"

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": "%(title)s.%(ext)s",
        "format_id": format_id,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            x = ydl.extract_info(yturl, download=False)

        title = (x["title"]).title()
        title = re.sub(r"\W+", " ", title)

        thumb_image_path = await CallbackQuery.message.download()

        duration = x["duration"]

        if stype == "video":
            ydl_opts["format"] = f"{format_id}+bestaudio"
        elif stype == "audio":
            ydl_opts["format"] = format_id

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            filename = ydl.prepare_filename(x)
            ydl.download([yturl])

        if stype == "video":
            med = InputMediaVideo(
                media=filename,
                duration=duration,
                width=x.get("width"),
                height=x.get("height"),
                thumb=thumb_image_path,
                caption=title,
                supports_streaming=True,
            )
        elif stype == "audio":
            med = InputMediaAudio(
                media=filename,
                caption=title,
                thumb=thumb_image_path,
                title=title,
                performer=x.get("uploader"),
            )

        await mystic.edit_text(_["song_11"])

        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_DOCUMENT,
        )

        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])

        os.remove(filename)

    except Exception as e:
        print(e)
        return await mystic.edit_text(_["song_9"].format(str(e)))
