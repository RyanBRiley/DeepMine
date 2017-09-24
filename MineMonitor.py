import pandas as pd 
import numpy as np
import time
import glob
import StatusEnum
import re
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

	def generate_structure(self, update_num):
		update = []
		fail_count = []
		caution_count = []
		# Set the date as the first element.
		update_raw = self.data[0].iloc[update_num]
		update.append(update_raw['Date'])

		for i in xrange(4): # autoclave
			update.append({})
			fail_count.append({})
			caution_count.append({})
			update[i+1]["status"] = None
			for j in xrange(7): # agitator
				update[i + 1][chr(j+65)]={'status' : None}
				fail_count[i][chr(j+65)] = 0
				caution_count[i][chr(j+65)] = 0
			update[i+1]["Other"] = {}

		return update, fail_count, caution_count


	#Takes an input file and simulates a live feed with a stated interval, outputs state of each sensor
	def get_update(self, update_num):
		# Get the data structure
		[update, fail_count, caution_count] = self.generate_structure(update_num)
		for autoclave_num in xrange(len(self.data)):
			# initialize the counts
			autoclave_caution_count = 0
			autoclave_fail_count = 0

			# get the data from the csv
			update_raw = self.data[autoclave_num].iloc[update_num]
			for col in self.data[autoclave_num].columns:

				# Skip the date
				if col == 'Date':
					continue
				
				# Regular expression to match single capital letters
				match = None
				result = re.search('\s[A-G]\s', col)
				if result != None:
					match = result.group(0)[1]
				else:
					match = "Other"

				# Get difference between mean and raw value
				df = abs(update_raw[col] - self.sensor_mean[autoclave_num][col])
				if df < self.sensor_std[autoclave_num][col]:
					status = StatusEnum.Status.Good
				elif df >= self.sensor_std[autoclave_num][col] and df < 2 * self.sensor_std[autoclave_num][col]:
					status = StatusEnum.Status.Caution
					if caution_count[autoclave_num].has_key(match):
						caution_count[autoclave_num][match] += 1
				else:
					status = StatusEnum.Status.Fail
					if fail_count[autoclave_num].has_key(match):
						fail_count[autoclave_num][match] += 1
				update[autoclave_num + 1][match][col] = [status, update_raw[col]]
			'''
			print 'caution_count:   '	
			print caution_count
			print '----------'
			print 'fail_count:     '
			print fail_count
			print '----------'	
			'''
			for key in caution_count[autoclav_num].keys():
				update[autoclave_num + 1][key]['status'] = StatusEnum.Status.Good

			for key in caution_count[autoclave_num].keys():
				if caution_count[autoclave_num][key] > 2:
					update[autoclave_num + 1][key]['status'] = StatusEnum.Status.Caution
					autoclave_caution_count += 1

			for key in fail_count[autoclave_num].keys():
				if fail_count[autoclave_num][key] > 2:
					update[autoclave_num + 1][key]['status'] = StatusEnum.Status.Fail
					autoclave_fail_count += 1


			if autoclave_fail_count > 0:
				autoclave_status = StatusEnum.Status.Fail
			elif autoclave_caution_count > 2:
				autoclave_status = StatusEnum.Status.Caution
			else:
				autoclave_status = StatusEnum.Status.Good
			update[autoclave_num + 1]['status'] = autoclave_status
		print update[1]['Other']
		return update

if __name__ == '__main__':
    monitor = MineMonitor('data')
    monitor.learn_stats()
    monitor.get_update(2)
	#data = pd.read_csv('data/Autoclave_2_2017.csv', skiprows=3).convert_objects(convert_numeric=True)
	#monitor = MineMonitor(data)
	#monitor.learn_stats(data)
	#monitor.get_update(data, 2)
