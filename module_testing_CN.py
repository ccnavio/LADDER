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

	def armCopters(self, args):
		if( args == 1 )
			# arm 1 copter
		elif( args == 2 )
			# arm 2 copters
		elif( args == 3 )
			# arm 3 copters

def init(mpstate):
	"""initialize module"""
	return CmdtestModule(mpstate)
