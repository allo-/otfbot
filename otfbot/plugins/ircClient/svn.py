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
# (c) 2008 by Thomas Wiegart
#

"""
    Periodically checks a subversion repository for new revisions and posts them
"""

HAS_PYSVN=True
try:
    import pysvn
except ImportError:
    HAS_PYSVN=False

from otfbot.lib import chatMod

class Plugin(chatMod.chatMod):
    """ svn plugin """
    def __init__(self,bot):
        """
           Config has to look like this:
           svn.repositories.samplesvn.checkinterval: 30 (in Minutes!)
           svn.repositories.samplesvn.url: svn://url.to.your/svn
           
           and then do this in your channel-config:
           samplenetwork.'#samplechannel'.svn.repros: samplesvn
        
           and the bot will post updates of samplesvn in your channel.
           You can specify more repros just by appending them seperated with a comma.
        """
        self.bot = bot
        if not HAS_PYSVN:
            self.bot.depends("pysvn python module")
        self.callIds = {}
        self.svnconfig = self.bot.config.get("repositories", [], "svn")
    def joined(self,channel):
        repros = self.bot.config.get("repros","","svn",self.bot.network,channel)
        if repros != "":
            try:
                repros = repros.split(",")
            except:
                repros = [repros,]
            for i in repros:
                try:
                    lastrev = int(open(datadir + "/revision_" + channel + "_" + i).readlines()[0].replace("\n","").replace("\r",""))
                except:
                    lastrev = 0
                try:
                    self.callIds[i + "-" + channel] = self.bot.getServiceNamed('scheduler').callLater(1, self.svncheck, self.svnconfig[i]['url'],self.svnconfig[i]['checkinterval'],channel,i)
                except KeyError:
                    self.logger.warning("Repository " + i + " doen't exist!")
        
    def kickedFrom(self, channel, kicker, message):
        self.left(channel)
    def left(self, channel):
        repros = self.bot.config.get("repros", "", "svn", self.bot.network, channel)
        if repros != "":
            try:
                repros = repros.split(",")
            except:
                repros = [repros,]
            for i in repros:
                self.callIds[i + "-" + channel].cancel()
                self.logger.info("Canceled callLater '" + i + "-" + channel + "'")
    def connectionLost(self,reason):
        for i in self.callIds:
            self.callIds[i].cancel()
            self.logger.info("Canceled callLater '" + i + "'")
    def svncheck(self, url, interval, channels, name, lastrevision=0):
        """
            checks the repository for updates and post a message if something changed
        """
        try:
            data = pysvn.Client().log(url,limit=1)[0].data
            rev = data['revision'].number
        except:
            self.logger.warning("Client Error. Ensure the url is right.")
            rev = lastrevision
        channel = channels
        if rev != lastrevision:
            lastrevision = rev
            self.bot.msg(channel,chr(2) + "[" + str(name) + "]" + chr(2) + " Revision " + str(rev) + " by " + data['author'].encode() + ": " + data['message'].encode().replace("\n","").replace("\r",""))
            open(datadir + "/revision_" + channel + "_" + name,"w").writelines(str(lastrevision))
        self.callIds[name + "-" + channel] = self.bot.getServiceNamed('scheduler').callLater(int(interval)*60, self.svncheck, url, interval, channels, name, lastrevision)
