"""
    MAVProxy 
    Stephen Richards
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



def init(mpstate):
    '''initialise module'''
return TrafficModule(mpstate)
