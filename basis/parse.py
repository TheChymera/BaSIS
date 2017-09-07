from bs4 import BeautifulSoup
from os import path

def bluecover_gps(infile,
	save_as="output.csv",
	):
	"""Covert gpsapp `.csv` file to `.csv`.
	"""

	infile = path.abspath(path.expanduser(infile))

	with open(infile) as f:
		inlined = f.read().replace('\n', '')
	soup=BeautifulSoup(inlined, "lxml")

	wpts = soup.findAll("wpt")

	if save_as:
		with open(save_as, 'w') as f:
			for wpt in wpts:
				try:
					f.write(wpt.time.text + "," + wpt.extensions.tags.text + "\n")
				except:
					f.write(wpt.time.text + ", notag\n")

if __name__ == "__main__":
	bluecover_gps('~/Downloads/GPSWaypoints-2017-08-08.gpx')
