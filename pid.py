# PID 

# Point you want to be at
setpoint = 0

# Error in the system
error

# Time differential ( Set to 10 Hz )
dt = 0.1

# Measured value or what you read from sensors
measured_value = 10

# Gains
Kp = 1
Ki = 1
Kd = 0.01

# Control Loop
while error > 0.5
	error = setpoint - measured_value			# Difference between where you want to be from where you are
	integral += error*dt					# Sum of error from setpoint
	derivative = (error - previous_error)/dt		# How fast the error changes
	output = Kp*error + Ki*integral + Kd*derivative		# Response of the system
	if minimumThrust*abs(output) > 1700			# Is 1700 too much?
		continue
	# SendRC(1:4, minimumThrust*abs(output), True) 
	previous_error = error					# Reset previous error for derivative term next loop

