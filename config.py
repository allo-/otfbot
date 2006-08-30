#!/usr/bin/python
#
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

import handyxml

class config:
	#private
	def getoptions(self, optionlist):
		ret={}
		for option in optionlist:
			try:
				ret[option.name]=option.value
			except AttributeError:
				self.logger.error("Config Error: Option name or value missing")
		return ret
		
	def getsuboptions(self, list):
		ret={}
		for item in list:
			options=[]
			try:
				options=item.option
			except AttributeError:
				pass
			tmp=self.getoptions(options)
			try:
				ret[item.name]=tmp
			except AttributeError:
				self.logger.error("Config Error: network/channel has no name")
		return ret

	def sorted(self, list):
		"""returns the sorted list"""
		list.sort()
		return list

	#public
	def __init__(self, logging, filename=None):
		"""Initialize the config class and load a xml config"""
		self.logger=logging.getLogger("config")
		self.generic_options={}
		self.network_options={}
		self.channel_options={}
		if not filename:
			return
		
		self.doc=handyxml.xml(filename)
		#generic options
		options={}
		try:
			options=self.doc.option
		except AttributeError:
			pass
		self.generic_options=self.getoptions(options)
	
		#network specific
		networks=[]
		try:
			networks=self.doc.network
		except AttributeError:
			pass
		self.network_options=self.getsuboptions(networks);
	
		#channel specific (format = channel_options[network][channel])
		for network in networks:
			channels=[]
			try:
				channels=network.channel
			except AttributeError:
				pass
			try:
				self.channel_options[network.name]=self.getsuboptions(channels)
			except AttributeError:
				self.logger.error("Config Error: network has no name")
	
	def get(self, option, default, module=None, network=None, channel=None):
			if module:
				option=module+"."+option

			try:
				return self.channel_options[network][channel][option]
			except KeyError:
				pass
			try:
				return self.network_options[network][option];
			except KeyError:
				pass
			try:
				return self.generic_options[option];
			except KeyError:
				pass
			#set default in config, and return it
			if network and channel:
				if not network in self.channel_options.keys():
					self.channel_options[network]={}
				if not channel in self.channel_options[network].keys():
					self.channel_options[network][channel]={}
				self.channel_options[network][channel][option]=default
			elif network:
				if not network in self.network_options.keys():
					self.network_options[network]={}
				self.network_options[network][option]=default
			else:
				self.generic_options[option]=default
			return default
	
	def set(self, option, value, module=None, network=None, channel=None):
		if module:
				option=module+"."+option

		if network and channel:
			if not network in self.channel_options.keys():
				self.channel_options[network]={}
			if not channel in self.channel_options[network].keys():
				self.channel_options[network][channel]={}
			self.channel_options[network][channel][option]=value
		elif network:
			if not network in self.network_options.keys():
				self.network_options[network]={}
			self.network_options[network][option]=value
		else:
			self.generic_options[option]=value


	def	getNetworks(self):
		ret=[]
		for network in self.network_options.keys():
			ret.append(network)
		#it is not sure, that we have a network in network and channel options
		for network in self.channel_options.keys():
			if not network in ret:
				ret.append(network)
		return ret
	def getChannels(self, network):
		if network in self.channel_options.keys():
			try:
				return self.channel_options[network].keys()
			except AttributeError:
				return []

	def exportxml(self):
		ret="<?xml version=\"1.0\"?>\n"
		ret+="<!DOCTYPE config SYSTEM \"config.dtd\">\n"
		ret+="<chatbot>\n"
		indent="	";
		#generic options
		for option in sorted(self.generic_options.keys()):
			ret+=indent+"<option name=\""+option+"\" value=\""+self.generic_options[option]+"\" />\n"
			
		channel_networks=self.channel_options.keys() #list of networks with *channel* settings
		all_networks=self.network_options.keys() #list of *all* networks
		for network in channel_networks:
			if not network in all_networks:
				all_networks.append(network)
			
		for network in all_networks:
			ret+=indent+"<network name=\""+network+"\">\n"
			#network specific
			if network in self.network_options.keys():
				for option in sorted(self.network_options[network].keys()):
					ret+=indent*2+"<option name=\""+option+"\" value=\""+self.network_options[network][option]+"\" />\n"
			#channel specific
			if network in channel_networks:
				for channel in self.channel_options[network].keys():
					ret+=indent*2+"<channel name=\""+channel+"\">\n"
					for option in sorted(self.channel_options[network][channel].keys()):
						ret+=indent*3+"<option name=\""+option+"\" value=\""+self.channel_options[network][channel][option]+"\" />\n"
					ret+=indent*2+"</channel>\n"
			ret+=indent+"</network>\n"
		
		ret+="</chatbot>\n"
		return ret