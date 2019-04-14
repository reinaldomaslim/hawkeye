import os
import glob
import config
import time

### perform housekeeping matters for server, station, client
### if file in data folder more than some days, remove
print("Housekeeping Node, clean up old data")

files = glob.glob('./data/*/*/*')
now = time.time()

for path in files:
	print(path)
	modif_time = os.path.getmtime(path) 
	diff = now-modif_time	
	
	#diff in seconds
	if diff > config.housekeeping_days*24*3600:
		os.remove(path)
		print('deleted: '+path)
	
