pyPingPlacefile
===============

Creates a GR placefile of PING data

How it works:
-Downloads raw HTML from PING Display page
-Goes through ptype and hail reports, putting data into lists
-Outputs a CSVs for reports received in the past 15, 30, and 600 minutes

All reports are currently exported as CSVs in the format `latitude,longitude,preciptype,reporttime,hailsize`.
Hail size is only proivded if the preciptype is hail, logically.

The pingIcons.png is currently an unused iconset left over from forking this code from the original project.

**Future Enhancements**
* Output to KML and/or GeoJSON in addition to CSV
* Add a map page with which these reports can be viewed.