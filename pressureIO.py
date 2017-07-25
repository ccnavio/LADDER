import io
import os

i = 1
while os.path.exists( 'pressureReadings%s.txt' % i ):
	i += 1

with io.open( 'pressureReadings%s.txt' % i, 'w' ) as file:
	data = '%.2f' % cs.lat + ' ' + '%.2f' % cs.lng + ' ' + '%.2f' % cs.alt + ' ' + '%0.3f' % cs.press_abs 
	file.write(u"%s\n" % data)
	file.close()
