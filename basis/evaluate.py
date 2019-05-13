import pandas as pd

def occurrence_by_date(df,
	date_column='TDRC',
	resolution='M',
	):
	"""
	Count occurrences based on an occurrence-wise Pandas Dataframe (one occurrence per row), with a datetime column.
	"""

	new_date_column = 'Date [{}]'.format(resolution)
	df = df.rename(columns={date_column: new_date_column})
	df = df.dropna(subset=[new_date_column])
	df[new_date_column] = pd.to_datetime(df[new_date_column])
	df.set_index(new_date_column, inplace=True)
	df['occurrence'] = 1
	df = df.resample(resolution).apply({'occurrence':'count'})
	return df
