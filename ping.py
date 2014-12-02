#!/usr/bin/env python

# Scrapes data from the NSSL PING project website and converts it into CSV files containing reports
#    from the past 15, 30, and 600 minutes.
# Forked from https://github.com/wxjoe/pyPingPlacefile

# import stuff
import urllib, re, calendar, time
# misc prep
now = time.gmtime() # set year to this year; needed for baseTime
baseTime = calendar.timegm((int(time.strftime("%Y", now)),1,1,0,0,0,0,0,0))
nowTime = calendar.timegm((int(time.strftime("%Y", now)), int(time.strftime("%m", now)), int(time.strftime("%d", now)), int(time.strftime("%H", now)), int(time.strftime("%M", now)),0,0, 0,0))
ptypeLst = ["Hail","Test","None","Rain","Drizzle","Freezing Rain","Freezing Drizzle","Rain/Snow","Ice Pellets/Snow","Rain/Ice Pellets","Snow","Wet Snow","Ice Pellets","Graupel"]
### Step 1: Process the raw data ###############################################
# open PING homepage
raw = urllib.urlopen("http://www.nssl.noaa.gov/projects/ping/display/ping.php")
# remove top junk
daynum, timenum, lat, lon, ptype = [], [], [], [], []
rawtimenum = []
hailmag = []
print("::: File downloaded, now processing PING data")

for line in raw:
  if line[:2] == 'pr': # ptype report
    match = re.search('\[(.+?)\]\=\[(.+?)\,(.+?)\,(.+?)\,(.+?)\]',line)
    if match:
      daynum.append(match.group(1))
      rawtimenum.append(int(match.group(2)))
      timenum.append(time.strftime("%m/%d/%Y %H:%M UTC", time.gmtime(baseTime + (int(match.group(2))*60))))
      lat.append(match.group(3))
      lon.append(match.group(4))
      ptype.append(match.group(5))
      hailmag.append('-999') # placeholder
  elif line[:2] == 'hr': # hail report
    match = re.search('\[(.+?)\]\=\[(.+?)\,(.+?)\,(.+?)\,(.+?)\]',line)
    if match:
      daynum.append(match.group(1))
      rawtimenum.append(int(match.group(2)))
      timenum.append(time.strftime("%m/%d/%Y %H:%M UTC", time.gmtime(baseTime + (int(match.group(2))*60))))
      lat.append(match.group(3))
      lon.append(match.group(4))
      hailmag.append(match.group(5))
      ptype.append('0')

print("::: Done processing PING data, now creating output files")
print("--> Found " + str(len(daynum)) + " total reports")

# post-processing to grab latest x hours
minTime = min(rawtimenum)
maxTime = max(rawtimenum)
nowMinutes = (nowTime - baseTime) / 60
times = {}
times[15] = nowMinutes - 15
times[30] = nowMinutes - 30
times[600] = nowMinutes - 600
### Step 2: Create the placefile ##################################################
for t in times.keys():
  # For now just print out the report raw data
  print str(t)+"-min PING repotrts"
  filename = "csv/"+str(t)+"-min_ping_rpts.csv"
  fh = open(filename, 'w')
  reports = 0
  for i in range(len(daynum)):
    if(rawtimenum[i] > times[t]):
      reports += 1
      rptPtype = int(ptype[i])
      if(rptPtype <= 12):
        #print "Report "+str(i)+": Lat="+str(lat[i])+", Lon="+str(lon[i])+", Type="+str(ptypeLst[rptPtype])+", Time="+timenum[i]
        
        reportArr = [lat[i], lon[i], ptypeLst[rptPtype], timenum[i]]
        if(rptPtype == 0):
          reportArr.append(hailmag[i])

        reportStr = ','.join(reportArr)
        fh.write(reportStr+"\n")

  fh.close()
  print("--> Wrote "+str(reports)+" reports to file "+filename)

print("::: Done writing all output files.")