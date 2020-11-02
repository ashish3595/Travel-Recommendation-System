import csv
import os
import requests
import itertools
from datetime import datetime

#from writefile import NamedTemporaryFile
#import shutil

wunderground_api_key = '14fc547954e1a07e'

filename = "flickr_dataset_dbscan_10.csv"
#writefile = NamedTemporaryFile(delete=False)

new_rows_list = []

with open(filename, 'rb') as readfile:
	reader=csv.reader(readfile, delimiter=',')


	# input_file = readfile.readlines()
	
	
	# for x in input_file:
	# 	print x

	first_row_flag = True

	for row in reader:

		if first_row_flag:
			new_rows_list.append(row)
			first_row_flag = False
			continue
		
		date = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
		time24 = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S").time()
		time12 = time24.strftime("%I:%M %p")

		#print time12

		url = 'http://api.wunderground.com/api/' + wunderground_api_key + '/history_' + str(date.date()).replace("-", "") + '/q/Maharashtra/Mumbai.json'

		print url

		# time_to_check = ''

		# if date.minute / 30 == 0:
		# 	time_to_check = str(date.hour) + ":" + '00 ' + time12[6:]
		# else:
		# 	time_to_check = str(date.hour) + ":" + '30 ' + time12[6:]

		response = requests.get(url.decode("utf-8")).json()

		obs_list = response['history']['observations']

		index = 0

		for item in obs_list:
			to_verify = str(obs_list[index]['date']['pretty'])
			print to_verify
			
			if str(time12[0:1])=='0':
				#if first char is 0
				hour_check = str(time12[1:2])
			else:
				hour_check = str(time12[0:2])

			print hour_check + " " + str(time12[6:])

			if (to_verify.startswith(hour_check)) & (to_verify.find(str(time12[6:])) != -1):
				weather = response['history']['observations'][index]['conds']
				temp = response['history']['observations'][index]['tempm']
				print weather, temp
				data = [weather.encode('utf-8'), temp.encode('utf-8')]
				new_rows_list.append(sum([row, data], []))
				print new_rows_list
				break
			index += 1

	#shutil.move(writefile.name, filename)

readfile.close()

os.remove(filename)

with open(filename, 'a') as writefile:
	writer = csv.writer(writefile, delimiter=',')
	writer.writerows(new_rows_list)

writefile.close()

		