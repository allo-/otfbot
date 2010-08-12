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

"""
    Post something to the microblog identi.ca
"""

from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

LIB = True
try:
    import identi
except ImportError:
    LIB = False


class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        if not LIB:
            self.bot.depends_on_module("identi", "please download "+
                    "http://media.commandline.org.uk/code/identi.txt to "+
                    "lib/identi.py to use identica")

    @callback
    def command(self, user, channel, command, options):
        if not LIB:
            return
        if command in ["identica", "i", "identicawithnick", "iwn"]:
            #TODO: blocking
            u = self.bot.config.get("username", '', 'identica', self.bot.network, channel)
            p = self.bot.config.get("password", '', 'identica', self.bot.network, channel)
            self.api = identi.IdentiCA(u, p)
            #TODO: blocking
            self.api.login()
            if command == "iwn" or command == "identicawithnick":
                options = user.split("!")[0] + ": " + options
            options = options[:140]
            #TODO: blocking
            self.api.put_message(options)
