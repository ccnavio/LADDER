# THINGS THAT NEED TO BE DOUBLE CHECKED BEFORE FLIGHT

# Check that cs.timeInAir does what it's supposed to
# Check that you can still take control during attempted landings

# Safety Check SWITCH should work at ANY point in the script

# Check_status should stop script at any point if any of the following are actvated
	# max climbrate
	# max roll
	# max pitch
	# Altitude of 2 m

# Check the inital mode check
# Check max yaw limit for Control_yaw
# Check max roll limit for control_roll
	# Is roll limited by Check_status or by the if statement within the loop?

# Make sure every loop contains at least 1 check_status