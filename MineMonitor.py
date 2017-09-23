import pandas as pd 
import numpy as np
import time
#from sklearn.cluster import KMean
class Status(enum.Enum):
    Good = 1
    Caution = 2
    Fail = 3

class MineMonitor(): 
	sensors = []
	sensor_mean = {}
	sensor_std = {}

	def __init__(self, data):
		print "initializing instance of mine monitor\n------------------------"
		self.sensors = [sensor for sensor in data.columns.values[1:]]
		print self.sensors
		return

	#Calculates the mean and standard deviation for each sensor value
	def learn_stats(self, data):
		print "learning stats\n---------------"
		for sensor in self.sensors:
			self.sensor_mean[sensor] = np.mean(data[sensor][1:20].values.astype(np.float))
			self.sensor_std[sensor] = np.std(data[sensor][1:20].values.astype(np.float))
		print self.sensor_mean
		print self.sensor_std
		print "---------------"
		return

	#Takes an input file and simulates a live feed with a stated interval, outputs state of each sensor
	def monitor_feed(self, data, interval, start_index=1, end_index=21):
		update = []
		caution_count = 0
		fail_count = 0
		for update_num in xrange(start_index, end_index):
			for autoclav_num in xrange(len(data)):
				update_raw = data[autoclav_num].iloc[update_num]
				update[autoclav_num + 1] = {}
				for col in data[autoclav_num].columns:
					if col == 'Date':
						if not update[0]:
							update[0] = update_raw[col]
						continue
					df = abs(update_raw[col] - self.sensor_mean[col])
					if df < self.sensor_std[col]:
						status = Status.Good
					elif df >= self.sensor_std[col] and df < 2 * self.sensor_std[col]:
						status = Status.Caution
						caution_count += 1
					else:
						status = Status.Fail
						fail_count += 1 
					print status
					update[autoclav_num + 1][col] = [status, update_raw[col]]
				if fail_count > 2:
					autoclav_status = Status.Fail
				elif fail_count > 0 or caution_count > 2:
					autoclav_status = Status.Caution
				else:
					autoclav_status = Status.Good
				update[autoclav_num + 1]['status'] = autoclav_status
			time.sleep(interval)
		return update



if __name__ == '__main__':
	data = pd.read_csv('data/Autoclave_2_2017.csv', skiprows=3).convert_objects(convert_numeric=True)
	monitor = MineMonitor(data)
	monitor.learn_stats(data)
	monitor.monitor_feed(data, 2)
