import numpy as np
from sys import argv
import pandas as pd
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import AuthorRetrieval
import pickle
import datetime

def extract(name, surname, scopusid):

	#au = ScopusSearch('AUTH({}, {})'.format(surname, name[0]))
	au = ScopusSearch('AU-ID({})'.format(scopusid))
	df = pd.DataFrame(pd.DataFrame(au.results))
	return(df)

def main():

	authors = pd.read_csv(argv[1])

	#print(authors)

	totallist = pd.DataFrame(columns = ['eid', 'publicationName', 'title','coverDate'])
	#totallist = pd.DataFrame()
	
	for index, row in authors.iterrows():
		print(row)
		print(row['Scopus ID'])
		aulist = extract(row['Name'],row['Surname'],row['Scopus ID'])[['eid','publicationName','title','coverDate']]
		totallist = pd.concat([totallist,aulist],axis=0).reset_index(drop=True)

	totallist = totallist.drop_duplicates(subset=['eid']).reset_index()

	totallist['coverDate'] = totallist['coverDate'].apply(pd.to_datetime).dt.date
	totallist = totallist[totallist['coverDate'] > datetime.date(2018,1,1)]
	#print(totallist)

	journalcount = totallist['publicationName'].value_counts()
	journalcount.to_csv('out.csv')
	totallist.to_csv('fullout.csv')
	print(journalcount)

main()



