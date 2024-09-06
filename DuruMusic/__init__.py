#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/DuruMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/DuruMusic/blob/master/LICENSE >
#
# All rights reserved.

from DuruMusic.core.bot import DuruBot
from DuruMusic.core.dir import dirr
from DuruMusic.core.git import git
from DuruMusic.core.userbot import Userbot
from DuruMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()
# Bot Client
app = DuruBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
