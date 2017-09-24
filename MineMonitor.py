import pandas as pd 
import numpy as np
import time
import glob
import StatusEnum
#from sklearn.cluster import KMean

class MineMonitor(): 
	data = []
	sensors = []
	sensor_mean = []
	sensor_std = []

	def __init__(self, str_loc):
		print "---------------------initializing instance of mine monitor------------------------"
		auto_claves = ['1','2','3','4']
		for auto_clave in auto_claves:
			all_clean_files = glob.glob(str_loc + '/Autoclave_' + auto_clave + '_2015_clean.csv')
			for file in all_clean_files:
				print "Reading file: " + file
				self.data.append(pd.read_csv(file).convert_objects(convert_numeric=True))
		
		self.sensors = [sensor for sensor in self.data[0].columns.values[1:]]

	#Calculates the mean and standard deviation for each sensor value
	def learn_stats(self):
		print "-------------learning stats---------------"
		for autoclav_num in xrange(len(self.data)):
			self.sensor_mean.append({})
			self.sensor_std.append({})	
			count = 0
			for sensor in self.sensors:
				self.sensor_mean[autoclav_num][sensor] = np.nanmean(self.data[autoclav_num][sensor].values.astype(np.float))
				self.sensor_std[autoclav_num][sensor] = np.nanstd(self.data[autoclav_num][sensor].values.astype(np.float))
		return

	#Takes an input file and simulates a live feed with a stated interval, outputs state of each sensor
	def get_update(self, update_num):
		update = []
		caution_count = 0
		fail_count = 0
		for autoclav_num in xrange(len(self.data)):
			#print 'autoclav_num: ' + str(autoclav_num)
			update_raw = self.data[autoclav_num].iloc[update_num]
			if not update:
				update.append(update_raw['Date'])
			update.append({})
			for col in self.data[autoclav_num].columns:
				#print col
				#print update
				#print str(type(update_raw[col]))
				
				if col == 'Date':
					continue
				#print self.sensor_mean[autoclav_num][col]
				df = abs(update_raw[col] - self.sensor_mean[autoclav_num][col])
				#print df
				if df < self.sensor_std[autoclav_num][col]:
					status = StatusEnum.Status.Good
				elif df >= self.sensor_std[autoclav_num][col] and df < 2 * self.sensor_std[autoclav_num][col]:
					status = StatusEnum.Status.Caution
					caution_count += 1
				else:
					status = StatusEnum.Status.Fail
					fail_count += 1 
				update[autoclav_num + 1][col] = [status, update_raw[col]]
			if fail_count > 2:
				#print self.data[autoclav_num]['Date'][update_num]
				autoclav_status = StatusEnum.Status.Fail
			elif fail_count > 1 or caution_count > 3:
				autoclav_status = StatusEnum.Status.Caution
			else:
				autoclav_status = StatusEnum.Status.Good
			update[autoclav_num + 1]['status'] = autoclav_status	
		return update



if __name__ == '__main__':
    monitor = MineMonitor('data')
    monitor.learn_stats()
    monitor.get_update(2)
	#data = pd.read_csv('data/Autoclave_2_2017.csv', skiprows=3).convert_objects(convert_numeric=True)
	#monitor = MineMonitor(data)
	#monitor.learn_stats(data)
	#monitor.get_update(data, 2)
