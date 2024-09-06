
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, PING_IMG_URL
from DuruMusic import app
from DuruMusic.core.call import Duru
from DuruMusic.utils import bot_sys_stats
from DuruMusic.utils.decorators.language import language
from DuruMusic.utils.inline import support_group_markup


@app.on_message(filters.command(["ping", "alive", "ing", "live"], prefixes=["/", "!", "%", ",", "-", ".", "@", "#", "p", "P", "a", "A"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    start = datetime.now()
    pytgping = await Duru.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            resp,
            app.mention,
            UP,
            RAM,
            CPU,
            DISK,
            pytgping,
        ),
        reply_markup=support_group_markup(_),
    )
