from bs4 import BeautifulSoup
from os import path

def bluecover_gps_to_csv(infile,
	outfile="output.csv",
	):
	"""Covert gpsapp `.csv` file to `.csv`.
	"""

	infile = path.abspath(path.expanduser(infile))

	with open(infile) as f:
		x = f.read().replace('\n', '')
	y=BeautifulSoup(x, "lxml")

	wpts = y.findAll("wpt")
	with open(outfile, 'w') as f:
		for wpt in wpts:
			try:
				f.write(wpt.time.text + "," + wpt.extensions.tags.text + "\n")
			except:
				f.write(wpt.time.text + ", notag\n")

if __name__ == "__main__":
	from_gpsapp('~/Downloads/GPSWaypoints-2017-08-08.gpx')
