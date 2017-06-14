"""

MAVProxy Testing Multicopter Flight
Carie Navio
Rev. 1

"""
# C:\cygwin64\home\cnavio\ardupilot\modules\mavlink\pymavlink
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
	def __init__(self1,mpstate):
		"""initialize module"""
		super(CmdTestModule, self1).__init__(mpstate, "cmdlong")
		"""Commads for CmdTestmodule"""
		self1.add_command('takeoff', self1.cmd_takeoff, "takeoff")


def cmd_takeoff(self1, args):
	if (len(args) != 1):
		print("Testing: Specify altitude")
		return

	if (len(args) == 1):
		altitude = float(args[0])
		print("Take off on 1 started")
		self1.master.mav.command_test_send(
			self1.settings.target_system,  # target_system
                mavutil.mavlink.MAV_COMP_ID_SYSTEM_CONTROL, # target_component
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, # command
                0, # confirmation
                0, # param1
                0, # param2
                0, # param3
                0, # param4
                0, # param5
                0, # param6
                altitude) # param7

        print("Take off on 2 started")
		self2.master.mav.command_test_send(
			self2.settings.target_system,  # target_system
                mavutil.mavlink.MAV_COMP_ID_SYSTEM_CONTROL, # target_component
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, # command
                0, # confirmation
                0, # param1
                0, # param2
                0, # param3
                0, # param4
                0, # param5
                0, # param6
                altitude) # param7

def init(mpstate):
	"""initialize module"""
	return CmdtestModule(mpstate)