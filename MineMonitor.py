import pandas as pd 
import numpy as np
import time
import glob
#from sklearn.cluster import KMean


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
		update = {}
		for update_num in xrange(start_index, end_index):
			update_raw = data.iloc[update_num]
			for col in data.columns:
				if col == 'Date':
					continue
				df = abs(update_raw[col] - self.sensor_mean[col])
				if df < self.sensor_std[col]:
					status = 'green'
				elif df >= self.sensor_std[col] and df < 2 * self.sensor_std[col]:
					status = 'yellow'
				else:
					status = 'red'
				print status
			time.sleep(interval)
		return



if __name__ == '__main__':
    data = []
    auto_claves = ['1','2','3','4']
    
    for auto_clave in auto_claves:
        all_clean_files = glob.glob('data/Autoclave_' + auto_clave + '_2015*_clean.csv')
        for file in all_clean_files:
            print "Reading file: " + file
            data.append(pd.read_csv(file, skiprows=3).convert_objects(convert_numeric=True))

    
    #monitor = MineMonitor(data)
    #monitor.learn_stats(data)
    #monitor.monitor_feed(data, 2)
	#data = pd.read_csv('data/Autoclave_2_2017.csv', skiprows=3).convert_objects(convert_numeric=True)
	#monitor = MineMonitor(data)
	#monitor.learn_stats(data)
	#monitor.monitor_feed(data, 2)
