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
# (c) 2005, 2006 by Alexander Schier
#

class chatMod:
	def __init__(self, bot):
		self.bot=bot

	def auth(self, user):
		"""check the authorisation of the user"""
		pass
	def joined(self, channel):
		"""we have joined a channel"""
		pass
	def msg(self, user, channel, msg):
		"""message received"""
		pass
	def connectionMade(self):
		"""made connection to server"""
		pass
	def connectionLost(self,reason):
		"""lost connection to server"""
		pass
	def signedOn(self):
		"""successfully signed on"""
		pass
	def left(self, channel):
		"""we have left a channel"""
		pass
	def noticed(self, user, channel, msg):
		"""we got a notice"""
		pass
	def action(self, user, channel, message):
		"""action (/me) received"""
	def modeChanged(self, user, channel, set, modes, args):
		"""mode changed"""
		pass
	def userKicked(self, kickee, channel, kicker, message):
		"""someone kicked someone else"""
		pass
	def userJoined(self, user, channel):
		"""a user joined the channel"""
		pass
	def userLeft(self, user, channel):
		"""a user left the channel"""
		pass
	def yourHost(self, info):
		"""info about your host"""
		pass
	def userRenamed(self, oldname, newname):
		"""a user changed the nick"""
		pass
	def topicUpdated(self, user, channel, newTopic):
		"""a user changed the topic of a channel"""
		pass