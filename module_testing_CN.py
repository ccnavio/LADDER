"""

MAVProxy Testing Multicopter Flight
Carie Navio
Rev. 1

"""

import os, time, platform, math
from pymavlink import mavutil
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.mavproxy_map import mp_slipmap
from MAVProxy.modules.lib import mp_settings
from MAVProxy.modules.lib.mp_menu import *  # popup menus

if mp_util.has_wxpython:
    from MAVProxy.modules.lib.mp_menu import *

class CmdTestModule(mp_module.MPModule):
	def __init__(self,mpstate):
	"""initialize module"""
	super(CmdlongModule, self).__init__(mpstate, "cmdlong")
	"""Commads for CmdTestmodule"""

	# Method to arm the three copters
	# Doesn't work if you have less than 3 copters 
	def armCopters(self, coptersingal):
		# Set copters to a default of False or "off"
		self.copter1 = 0, self.copter2 = 0, self.copter3 = 0
		
		while( True ):
			# Stop once all signals have been received
			if( self.copter1 and self.copter2 and self.copter3 ):
				break
			
			# Copter 1's signal is 100, Copter 2's signal is 200, and Copter 3's signal is 300
			if( coptersignal == 100 ):
				self.copter1 = 1
			elif( coptersignal == 200 ):
				self.copter2 = 1
			elif( coptersignal == 300 ):
				self.copter3 = 1

def init(mpstate):
	"""initialize module"""
	return CmdtestModule(mpstate)
