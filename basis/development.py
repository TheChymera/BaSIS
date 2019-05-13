def id3():
	from parse import from_id3
	import matplotlib.pyplot as plt
	from evaluate import occurrence_by_date
	import pandas as pd
	df = from_id3('~/.dummydata/id3')
	df = occurrence_by_date(df)
	df = df.rename(columns={'occurrence': 'a'})
	lays = pd.read_csv('/home/chymera/.dummydata/secondary.csv')
	lays = occurrence_by_date(lays, date_column='first lay')
	lays = lays.rename(columns={'occurrence': 'l'})
	new_df = pd.merge(df, lays, how='outer', left_index=True, right_index=True)
	new_df['l'].fillna(0, inplace=True)
	new_df['a'].plot()
	new_df['l'].plot(secondary_y=True)
	plt.savefig('foo.png')

def gps():
	from parse import bluecover_gps
	bluecover_gps('~/Downloads/GPSWaypoints-2017-08-08.gpx')

def fl():
	from parse import fl
	fl('~/Downloads/ly.html',save_as="~/pu_data/text/")
