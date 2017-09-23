import pandas as pd 
import numpy as np
import time
import glob
import StatusEnum
#from sklearn.cluster import KMean

class MineMonitor(): 
	sensors = []
	sensor_mean = []
	sensor_std = []

	def __init__(self, data):
		print "---------------------initializing instance of mine monitor------------------------"
		#print data[0].columns
		self.sensors = [sensor for sensor in data[0].columns.values[1:]]
		#print self.sensors
		return

	#Calculates the mean and standard deviation for each sensor value
	def learn_stats(self, data):
		print "-------------learning stats---------------"
		for autoclav_num in xrange(len(data)):
			self.sensor_mean.append({})
			self.sensor_std.append({})	
			for sensor in self.sensors:
				print 'sensor: ' + sensor
				self.sensor_mean[autoclav_num][sensor] = np.mean(data[autoclav_num][sensor].values.astype(np.float))
				self.sensor_std[autoclav_num][sensor] = np.std(data[autoclav_num][sensor].values.astype(np.float))
		return

	#Takes an input file and simulates a live feed with a stated interval, outputs state of each sensor
	def get_update(self, data, update_num):
		update = []
		caution_count = 0
		fail_count = 0
		for autoclav_num in xrange(len(data)):
			print 'autoclav_num: ' + str(autoclav_num)
			update_raw = data[autoclav_num].iloc[update_num]
			if not update:
				update.append(update_raw['Date'])
			update.append({})
			for col in data[autoclav_num].columns:
				if col == 'Date':
					continue
				print update_raw[col]
				print self.sensor_mean[autoclav_num][col]
				df = abs(update_raw[col] - self.sensor_mean[autoclav_num][col])
				if df < self.sensor_std[autoclav_num][col]:
					StatusEnum.Status = StatusEnum.Status.Good
				elif df >= self.sensor_std[autoclav_num][col] and df < 2 * self.sensor_std[autoclav_num][col]:
					StatusEnum.Status = StatusEnum.Status.Caution
					caution_count += 1
				else:
					StatusEnum.Status = StatusEnum.Status.Fail
					fail_count += 1 
				print update
				update[autoclav_num + 1][col] = [StatusEnum.Status, update_raw[col]]
			if fail_count > 2:
				autoclav_status = StatusEnum.Status.Fail
			elif fail_count > 0 or caution_count > 2:
				autoclav_status = StatusEnum.Status.Caution
			else:
				autoclav_status = StatusEnum.Status.Good
			update[autoclav_num + 1]['StatusEnum.Status'] = autoclav_status	
		return update



if __name__ == '__main__':
    data = []
    auto_claves = ['1','2','3','4']
    
    for auto_clave in auto_claves:
        all_clean_files = glob.glob('data/Autoclave_' + auto_clave + '_2015*_clean.csv')
        for file in all_clean_files:
            print "Reading file: " + file
            data.append(pd.read_csv(file).convert_objects(convert_numeric=True))
    monitor = MineMonitor(data)
    monitor.learn_stats(data)
    print monitor.get_update(data, 2)
	#data = pd.read_csv('data/Autoclave_2_2017.csv', skiprows=3).convert_objects(convert_numeric=True)
	#monitor = MineMonitor(data)
	#monitor.learn_stats(data)
	#monitor.get_update(data, 2)
