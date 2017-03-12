#!/usr/bin/env python3

import requests
import time

def expand():
	url = 'http://www.omdbapi.com/'
	with open('movie_titles.txt', encoding='ISO-8859-1') as movies:
		for index, line in enumerate(movies):
			l = line.strip('\n')
			parts = l.split(',')
			id_num = parts[0]
			year = parts[1]
			title = parts[2]
			data = { 't': title, 'y': year }
			r = requests.get(url, params=data)
			try:
				r.raise_for_status()
				response = r.json()
				if response['Title'].lower() != title.lower():
					raise Exception('Not the movie')
				retrieved = [id_num,\
							title,\
							year,\
							response['Genre'],\
							response['Actors'],\
							response['Director'],\
							response['Writer'],\
							response['Language'],\
							response['Country'],\
							response['Type']]
				expanded_info = '|'.join(retrieved)
				with open('expanded_movies.txt', 'a') as expanded:
					expanded.write(expanded_info + '\n')
			except:
				with open('couldnt_expand.txt', 'a') as couldnt:
					couldnt.write(line)
			time.sleep(2)

if __name__ == '__main__':
	expand()