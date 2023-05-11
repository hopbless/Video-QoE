
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import json
import numpy as np
import csv
import os
import pandas as pd


CONFIGFILE = 'config'
EXPCONFIG = {"ytId":"Q_AeDvbjFsI",
"duration":60,
"bitrates":"144p:110.139,240p:246.425,360p:262.750,480p:529.500,720p:1036.744,1080p:2793.167"
}

header = ['avgBitrate', 'maxBitrate', 
	  'minBitrate','q25_bitrate','q50_bitrate', 'q75_bitrate' ,'q90_bitrate',
	  'avgBuffer','maxBuffer','minBuffer','q25_buffer', 'q50_buffer','q75_buffer','q90_buffer',
	  'numOfStallings','avgStalling','maxStalling', 'minStalling','q25_stalling','q50_stalling','q75_stalling' ,'q90_stalling']


def run_video():
	print (time.time(), ' start display')
    #display.start()
	time.sleep(10)

	# get url
	url2 = 'https://www.youtube.com/watch?v=' + EXPCONFIG['ytId']
	url = 'https://www.w3.org/2010/05/video/mediaevents.html'
    #'https://www.w3.org/2010/05/video/mediaevents.html'

	# set file prefix
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	prefix = "YT_" + EXPCONFIG['ytId'] + '_' + st

    # define chrome settings
	caps = DesiredCapabilities.CHROME.copy() 
	caps['acceptInsecureCerts'] = True
	#caps["pageLoadStrategy"] = "normal"  #  complete
	caps["pageLoadStrategy"] = "none"
    
	try:
		print(time.time(), ' start chrome')
		#s = Service(ChromeDriverManager().install())
		service = Service(executable_path="chromedriver.exe")
		browser = webdriver.Chrome(executable_path='chromedriver.exe', desired_capabilities=caps)
		#browser = webdriver.Chrome(desired_capabilities=caps)
		browser.maximize_window()
		time.sleep(10)

			# read in js
		jsFile = open('opt/pluginAsJS.js', 'r')
		js = jsFile.read()
		jsFile.close

			# open webpage
		print (time.time(), ' start video ', EXPCONFIG['ytId'])
		browser.get(url)
		browser.get_screenshot_as_file('results/screenshot0.png')

			# inject js
		browser.execute_script(js)
		duration = EXPCONFIG['duration']
		time.sleep(duration)
			
			# get infos from js and write to file
		print ("video playback ended")
		out = browser.execute_script('return document.getElementById("outC").innerHTML;')
		outE = browser.execute_script('return document.getElementById("outE").innerHTML;')
			#print("OUT from js", outE.encode("UTF-8"))
		with open('results/' + prefix + '_buffer.txt', 'w') as f:
				f.write(out)

		with open('results/' + prefix + '_events.txt', 'w') as f:
				f.write(outE)
					
				# close browser
		browser.close()
		print (time.time(), ' finished chrome')
	    
	except Exception as e:
			print(time.time(), ' exception thrown')
			print(e)
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
			print(st)
		
			# stop display
			
			#display.stop()
			

	bitrates = EXPCONFIG['bitrates'].split(",")

	# with open('data/streams.csv', 'w') as file:
	# 	writer = csv.writer(file, delimiter=",")
	# 	writer.writerow(header)
	# 	writer.writerow([getOutput(prefix, bitrates)])

	with open('_outStream.txt', 'w') as f:
		f.write(getOutput(prefix, bitrates))
	
	df = pd.read_csv('_outStream.txt',names=header, sep=',', header=None)
	df.to_csv('data/streams.csv')
	

	return


# Calculate average, max, min, 25-50-75-90 quantiles of the following: bitrate [KB], buffer [s], number of stalls, duration of stalls

def getOutput(prefix, bitrates):
	bitrate = calculateBitrate(prefix, bitrates)
	buffer = calculateBuffer(prefix)
	stalled = calculateStallings(prefix)
	#print("buffer", buffer)
	out = bitrate + "," + buffer + "," + stalled
	os.remove("results/" + prefix + "_events.txt")
	os.remove('results/' + prefix + '_buffer.txt')

	return out

def getEvents(prefix):
	timestamps = []
	qualities = []
	with open('results/' + prefix + "_events.txt", "r") as filestream:
		for line in filestream:
			currentline = line.split("#")
			if ("quality" in currentline[1]): 
				timestamps.append(float(currentline[0]))
				quality = str(currentline[1])
				quality = quality.split(":")[1]
				quality = quality.split(" ")[0]
				qualities.append(quality)
			if ("ended" in currentline[1]):
				endtime = float(currentline[0])
	if 'endtime' not in locals():
		[times, playtime, buffertime, avPlaytime] = getBuffer(prefix)
		endtime = times[-1]
	return [timestamps, qualities, endtime]


def getBuffer(prefix):
	timestamps = []
	playtime = []
	buffertime = []
	avPlaytime = []
	isFirstLine = True
	with open('results/' + prefix + "_buffer.txt", "r") as filestream:
		for line in filestream:
			currentline = line.split("#")
			# end of video
			if (isFirstLine is False and float(currentline[1]) == playtime[-1]): #TODO 
				break;
			timestamps.append(float(currentline[0]))
			playtime.append(float(currentline[1]))
			buffertime.append(float(currentline[2]))
			avPlaytime.append(float(currentline[3][:-1]))
			isFirstLine = False
	return [timestamps , playtime, buffertime, avPlaytime]

def calculateBitrate(prefix, bitrates):
	[timestamps, qualities, endtime] = getEvents(prefix)
	timestamps.append(endtime)
	periods = [x / 1000 for x in timestamps]
	periods = np.diff(periods)
	periods = np.round(periods)
	periods = [int(i) for i in periods]
		
	usedBitrates = []	
	
	for x in range(0,len(qualities)):
		index = [i for i, j in enumerate(bitrates) if qualities[x] in j]
		currRate = float(bitrates[index[0]].split(":")[1])
		usedBitrates.extend([currRate] * periods[x])
		
	avgBitrate = sum(usedBitrates)/len(usedBitrates)
	maxBitrate = max(usedBitrates)
	minBitrate = min(usedBitrates)
	q25 = np.percentile(usedBitrates, 25)
	q50 = np.percentile(usedBitrates, 50)
	q75 = np.percentile(usedBitrates, 75)
	q90 = np.percentile(usedBitrates, 90)
	return str(avgBitrate) + "," + str(maxBitrate) + "," + str(minBitrate) + "," + str(q25) + "," + str(q50) + "," + str(q75) + "," + str(q90)

def calculateBuffer(prefix):
	[timestamps , playtime, buffertime, avPlaytime] = getBuffer(prefix)	
	avgBuffer = sum(buffertime)/len(buffertime)
	maxBuffer = max(buffertime)
	minBuffer = min(buffertime)
	q25 = np.percentile(buffertime, 25)
	q50 = np.percentile(buffertime, 50)
	q75 = np.percentile(buffertime, 75)
	q90 = np.percentile(buffertime, 90)
	return str(avgBuffer) + "," + str(maxBuffer) + "," + str(minBuffer) + "," + str(q25) + "," + str(q50) + "," + str(q75) + "," + str(q90) 

def calculateStallings(prefix):
	[timestamps , playtime, buffertime, avPlaytime] = getBuffer(prefix)
	diffTimestamps = np.diff(timestamps)/1000
	diffPlaytime = np.diff(playtime)

	diffTimePlaytime = diffTimestamps - diffPlaytime
	stallings = [0]
	for i in diffTimePlaytime:
		if (i > 0.5):
			stallings.append(i)
		
	numOfStallings = len(stallings)
	avgStalling = sum(stallings)/len(stallings)
	maxStalling = max(stallings)
	minStalling = min(stallings)
	q25 = np.percentile(stallings, 25)
	q50 = np.percentile(stallings, 50)
	q75 = np.percentile(stallings, 75)
	q90 = np.percentile(stallings, 90)
	return str(numOfStallings) + "," + str(avgStalling) + "," + str(maxStalling) + "," + str(minStalling) + "," + str(q25) + "," + str(q50) + "," + str(q75) + "," + str(q90)



try:
    with open(CONFIGFILE) as configfd:
        EXPCONFIG.update(json.load(configfd))
except Exception as e:
    print ("Cannot retrive expconfig {}".format(e), "-- use defaulte settings")

if __name__ == '__main__':
	run_video()