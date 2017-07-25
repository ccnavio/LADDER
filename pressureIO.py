import io
import os

i = 1
while os.path.exists( 'pressureReadings%s.txt' % i ):
	i += 1

with io.open( 'pressureReadings%s.txt' % i, 'w' ) as file:
	data = str(cs.lat) + ' ' + str(cs.lng) + ' ' + str(cs.alt) + ' ' + str(cs.press_abs) + '\n' 
	file.write(u"%s" % data)
	file.close()
