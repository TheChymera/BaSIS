import pandas as pd
import re
from bs4 import BeautifulSoup
from hashlib import sha256
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

def fl(infile,
	anonymize=True,
	anonymous_filename=True,
	save_as="",
	):
	"""Convert an HTML page containing messages from the fl platform to a pandas DataFrame with messages on rows and attributes on columns.

	Parameters
	----------
	infile : str
		Path to the messages file (message pages are best saved to file via right-click and "save as" in your browser; only the file ending in `.html` is required here).
	anonymize : bool, optional
		Whether to remove every field which can unambiguously identify the sender, and represent identity as a complex hash of these fields and a hard-coded salt.
	anonymous_filename : bool, optional
		Whether to name the file according to the contained anonymous identities.
		If this is `True`, the path passed to the `save_as` parameter will be treated as a directory, and a file with the anonymous filename will be created inside it.
	save_as : str, optional
		Whether to save the conversation to file (in comma separated values format).
	"""

	match_strings=[
		r'^<span><a href="https://\S+\.\S+/users/(?P<id>.+)">(?P<alias>.*?)</a></span>',
		r'^<span class="quiet">(?P<age>\d+)(?P<gender>[\s\S]+)</span>$',
		r'^<p>(?P<content>.*?)</p>',
		r'^<div class="quiet"> <span>.*?written <time class="refresh-timestamp initialized" data-timestamp=".*?datetime="(?P<datetime>.*?)" title=".*?$',
		]

	infile = path.abspath(path.expanduser(infile))

	with open(infile) as f:
		inlined = f.read().replace('\n', '')

	html_soup = BeautifulSoup(inlined, "html.parser")
	html_good = html_soup.prettify()
	my_divs = html_soup.find_all('div', attrs={"class":"clearfix message"})
	messages = []
	for my_div in my_divs:
		message = {}
		children = [i for i in my_div.children]
		for child in children:
			try:
				sub_children = [i for i in child.children]
			except AttributeError:
				continue
			for ix, sub_child in enumerate(sub_children):
				text = str(sub_child)
				for match_string in match_strings:
					if re.match(match_string, text):
						m = re.match(match_string, text)
						m_dict = m.groupdict()
						if list(m_dict.keys()) == ['content']:
							try:
								m_dict['content'] = message['content']+'\n\n'+m_dict['content']
							except KeyError:
								pass
							m_dict['content'] = m_dict['content'].replace('<br/>','\n')
						message.update(m_dict)
		messages.append(message)

	messages = pd.DataFrame.from_dict(messages)
	messages = messages.set_index(pd.DatetimeIndex(messages['datetime']))
	messages = messages.drop(['datetime'], 1)
	if anonymize or anonymous_filename:
		messages['aid'] = messages['id']+messages['alias']+'fl'
		messages['aid'] = [sha256(val.encode('utf-8')).hexdigest()[:8] for val in messages['aid']]
	if anonymous_filename:
		aids = list(messages['aid'].unique())
		filename = "_".join(aids)

	if anonymize:
		messages = messages.drop(['alias','id'], 1)
	else:
		messages = messages.drop(['aid'], 1)

	if save_as:
		save_as = path.abspath(path.expanduser(save_as))
		if anonymous_filename:
			save_as = path.join(save_as,filename+'.csv')
		messages.to_csv(save_as)

	print(messages)
	return messages
