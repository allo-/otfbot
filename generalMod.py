#Copyright (C) 2005 Alexander Schier
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import random, re
import chatMod

class chatMod(chatMod.chatMod):
	def __init__(self, bot):
		self.bot=bot

	def joined(self, channel):
		#self.channel = channel
		pass

	def msg(self, user, channel, msg):
		#if channel == self.bot.nickname:
		if self.bot.auth(user):
			if msg == "!stop":
				self.bot.quit("War schoen euch kennengelernt zu haben.")
			if msg[0:5] == "!join":
				self.bot.join(msg[6:]) #does not include the space
			if msg[0:5] == "!part":
				self.bot.part(msg[6:])
			
		if msg == "!wuerfel":
			self.bot.sendme(channel, "wuerfelt. Das Ergebnis ist: "+str(random.randint(1,6)))
		elif msg[0:8] == "!wuerfel":
			num = 2
			string = "wuerfelt. Die Ergebnisse sind: "
			try:
				num = int(msg[8:])
			except ValueError:
				num = 2
			if num > 10:
				num = 10
			for i in range(1,num+1):
				zahl = random.randint(1,6)/s
				if i < num:
					string += str(zahl)+", "
				else:
					string += str(zahl)
			self.bot.sendme(channel, string) 
