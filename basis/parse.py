import pandas as pd
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
	wpts = soup.find_all("wpt")

	wpt_dicts=[]
	for wpt in wpts:
		wpt_dict={}
		wpt_dict["lat"] = float(wpt["lat"])
		wpt_dict["lon"] = float(wpt["lon"])
		wpt_dict["ele"] = float(wpt.ele.text)
		wpt_dict["accuracy"] = float(wpt.accuracy.text)
		wpt_dict["time"] = wpt.time.text
		try:
			tag_text = wpt.extensions.tags.text
		except AttributeError:
			pass
		else:
			try:
				first, second = tag_text.split(",")
			except ValueError:
				first = tag_text
			if any(i in first for i in '123'):
				wpt_dict["looks"] = first[0]
				wpt_dict["person"], wpt_dict["interaction"] = second.split(" ")
			else:
				wpt_dict["person"], wpt_dict["interaction"] = first.split(" ")
				wpt_dict["looks"] = second[0]

		wpt_dicts.append(wpt_dict)

	df = pd.DataFrame.from_dict(wpt_dicts)
	df["time"] = pd.to_datetime(df["time"])

	if save_as:
		save_as = path.abspath(path.expanduser(save_as))
		df.to_csv(save_as)

