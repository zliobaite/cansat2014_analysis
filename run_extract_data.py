# 2014 10 21 I.Zliobaite
# extracts cansat data

#RUN: python run_extract_distribution.py

file_data = "2014-10-18 14-30-47.txt"

from collections import defaultdict
import math
import numpy as np
import time, datetime
import matplotlib.pyplot as plt

#param_filter = 'mavlink_global_position_int_t'
param_filter = 'mavlink_gps_raw_int_t'
do_filter = 0
ind0 = 2558
ind1 = 3844
param_plot_what = 'alt'
out_file_name = 'data.csv'


#print geo_distance(lat[0],lon[0],lat[108000],lon[108000]) - veikia
def geo_distance(lat1,lon1,lat2,lon2):
	rearth = 6371 #Earth Radius in km
	#print(lat1,lon1,lat2,lon2)
	inner1 = math.cos(radians(lat1)) * math.cos(radians(lat2))*math.cos(radians(lon2-lon1))
	inner2 = math.sin(radians(lat1))*math.sin(radians(lat2))
	insum = min(1.0,(inner1+inner2))
	dist = rearth*math.acos(insum)
	#Dist = 6378 * ACOS(COS(LatA) * COS(LatB) * COS(LngB - LngA) + SIN(LatA) * SIN(LatB))
	return dist

def radians(degrees):
	rr = 1.0*degrees*math.pi/180
	return rr

#read file
time_stamp = []
time_raw = []
lat = []
lon = []
alt = []
f = open(file_data)
lines = f.readlines()
for ln in lines:
	parts = ln.strip().split(' ')
	sk = 0
	found_gps = 0
	for pt in parts:
		if pt==param_filter:
			found_gps=1
			ts = datetime.datetime.strptime(parts[1], "%H:%M:%S")
			if len(time_stamp)==0:
				ts0 = ts #+ datetime.timedelta(seconds = 1000) #iki 607
				time_stamp.append(10000)
				time_raw.append('na')
			else:
				delta_t = ts - ts0
				time_stamp.append(int(delta_t.seconds))
				time_raw.append(ts)
			#print time_stamp[-1], parts[1]
		if found_gps==1:
			if pt=='lat':
				lat.append(float(parts[sk+1])*1.0/10000000)
			if pt=='lon':
				lon.append(float(parts[sk+1])*1.0/10000000)
			if pt=='alt':
				alt.append(float(parts[sk+1])*1.0/1000000)
		sk += 1
	#if len(alt)>0:
	#print lon[-1], lat[-1], alt[-1]
f.close()

lat = np.array(lat)
lon = np.array(lon)
alt = np.array(alt)
time_stamp = np.array(time_stamp)
print np.shape(lat), np.shape(lon), np.shape(alt), np.shape(time_stamp)
#ind = np.nonzero(lat > 0)

if do_filter:
	lat = lat[ind0:ind1+1]
	lon = lon[ind0:ind1+1]
	alt = alt[ind0:ind1+1]
	time_stamp = time_stamp[ind0:ind1+1]

time_stamp[0] = time_stamp[1]
time_stamp = time_stamp - time_stamp[0]
time_stamp = time_stamp*1.0/60 #min
#for aa in alt:
#print aa

print time_raw[-35],time_raw[-1]
print time_stamp[-35],time_stamp[-1]

alt_speed = []
ground_speed = []

for sk in range(len(lat)):
	if sk==0:
		alt_speed_now = 0
		ground_speed_now = 0
		alt_before = alt[0]
		time_before = time_stamp[0]
		lat_before = lat[0]
		lon_before = lon[0]
	else:
		d_time = time_stamp[sk] - time_before
		if d_time>0:
			d_alt = -alt[sk] + alt_before
			d_ground = geo_distance(lat_before,lon_before,lat[sk],lon[sk])
	
			alt_before = alt[sk]
			time_before	= time_stamp[sk]
			lat_before = lat[sk]
			lon_before = lon[sk]
		
			d_time = d_time*60.0 # in s
			d_alt = d_alt*1000.0 #in m
			d_ground = d_ground*1000.0 #in m
			print d_alt
	
			alt_speed_now = d_alt/d_time
			ground_speed_now = d_ground/d_time
	alt_speed.append(alt_speed_now)
	ground_speed.append(ground_speed_now)

f = open(out_file_name,'w')
for sk in range(len(lat)):
	f.write(str(time_stamp[sk])+' '+str(lat[sk])+' '+str(lon[sk])+' '+str(alt[sk])+' '+str(alt_speed[sk])+' '+str(ground_speed[sk])+'\n')
f.close()


#plt.plot(time_stamp, alt)
#plt.axis([xmin, xmax, ymin, ymax])
#plt.plot(time_stamp, alt, 'ro')
plt.plot(time_stamp, lon, 'ro')
#plt.plot(lat, lon, 'ro')
plt.xlabel('Time (min)')
plt.ylabel('Altitude (km)')
plt.title(param_filter)
#plt.savefig('altitude__'+param_filter+'.png')
plt.savefig('test.png')


