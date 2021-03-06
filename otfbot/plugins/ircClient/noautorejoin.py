# This file is part of OtfBot.
#
# OtfBot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# OtfBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OtfBot; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# (c) 2011 by Alexander Schier
#

"""
    ban users who use autorejoin
"""

class Meta:
    service_depends = ['scheduler']

from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

import time


class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.kicked_users={}

    @callback
    def userKicked(self, kickee, channel, kicker, message):
        self.kicked_users[kickee.lower()]=time.time()
    @callback
    def userJoined(self, user, channel):
        nick=user.getNick().lower()
        if nick in self.kicked_users and \
        time.time() - self.kicked_users[nick] < \
        self.bot.config.get("minwait", 2, "noautorejoin", \
        self.bot.network, channel): #fast rejoin
            self.bot.mode(channel, True, "b", mask="*!*@"+user.getHost())
            self.bot.kick(channel, nick, "do not use autorejoin")
            self.bot.root.getServiceNamed('scheduler').callLater(
                self.bot.config.get("unbandelay", 60, "noautorejoin",
                self.bot.network, channel),
                self.bot.mode, channel, False, "b", mask="*!*@"+user.getHost())
