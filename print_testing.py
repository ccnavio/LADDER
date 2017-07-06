# Carie Navio
# Mission Planner Script
# Purpose: Printing to File
# THIS DOES NOT INCLUDE THE UNLINKING PORTION

# This will remain pretty much untouched because we know how it works
# so if we run into issues, this program will help determine if they
# are code based, or hardware based.

import time

def Safety_Check():
	if cs.ch7in > 1800:
		for chan in range(1,9):
			Script.SendRC(chan,0,True)
		Script.Sleep(25)
		print 'Safety Override'
		exit()
	else:
		return 0

def Looping_Safety(time):
	loop_var = 0
	while_var = 0
	while_var = time/50
	while loop_var < while_var:
		Safety_Check()
		Script.Sleep(50)
		loop_var = loop_var + 1
	print 'End Safety Loop'

# --------------------------------- MAIN PROGRAM --------------------------------- #
save_path = "c:/Users/cnavio/Desktop/Logs/print_testing/"
file_name = time.strftime("%m-%d-%Y_%H-%M-%S")
complete_path = save_path+file_name+".txt"
print complete_path
f = open(complete_path, "w")

print 'Starting Script'
f.write("Starting Script")
# implement for all channels from 1-9

while cs.ch7in < 1800:
	f.write("%d\n" % cs.ch3in)
	Script.Sleep(50)
	print cs.ch3in

print 'Script Over'

f.close()
