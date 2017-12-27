def gps():
	from parse import bluecover_gps
	bluecover_gps('~/Downloads/GPSWaypoints-2017-08-08.gpx')

def fl():
	from parse import fl
	fl('~/Downloads/ly.html',save_as="~/pu_data/text/")
