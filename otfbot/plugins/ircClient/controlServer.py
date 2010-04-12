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
# (c) 2008 by Alexander Schier
#

from otfbot.lib import chatMod
import time

class Plugin(chatMod.chatMod):
    def __init__(self, bot):
        self.bot=bot
        self.getServers=lambda: [connection.kwargs['factory'].protocol for connection in bot.root.getServiceNamed('ircServer').services]

    def irc_unknown(self, prefix, command, params):
        if command=="PONG":
                for server in self.getServers():
                    server.sendmsg(self.bot.nickname+"!bot@localhost", "#control", "%f sec. to %s."%(round(time.time()-float(params[1]), 3), params[0]))
