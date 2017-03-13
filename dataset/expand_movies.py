#!/usr/bin/env python3

# A script to fetch a movie's genre, actors, director, writer, language, country, and type (movie/series)
# from the Open Movie Database, which gets its data from IMDb.
# ==========================================================================================================
# To run, simply:
# 	$ chmod a+x expand_movies.py
#	$ ./expand_movies.py -s ID_OF_FIRST_MOVIE_TO_FETCH -f PATH_OF_MOVIE_TITLES_FILE -en ENCODING
# 	  -exp PATH_OF_SUCCESSFUL_EXPANDED_MOVIES_OUTPUT -fail PATH_OF_FAILED_ENTRIES_OUTPUT
# If run without -s/--start, it will start from the very beginning.
# If run without -f/--file, it will use 'movie_titles.txt' in the same dir.
# If run without -en/--encoding, it will assume the file is ISO-8859-1 encoded.
# If run without -exp/--oexpanded, it will output successful entries in 'expanded_movies.txt' in the same dir.
# If run without -fail/--ofailed, it will output failed entries in 'couldnt_expand.txt'.
# This has to run with a movie title file provided, where each movie is on a new line in the following format:
# 	id,year_of_release,name
# ===========================================================================================================
# Expected output:
# 	- A file in the same dir called expanded_movies.txt which has the data of every movie on a new line.
#	  Order is shown in the code here and fields are separated with a |.
# 	  If a movie does not have a certain field, it will contain 'N/A' as the value of the field.
# 	- Another file (if applicable) in the dir called couldnt_expand.txt containing the data of the movies
# 	  the script couldn't expand (not found in OMDb, found but not the same movie title, etc)
# 	- In case of connectivity issues with the database, it will try again after 30 seconds (indefinitely)
# ===========================================================================================================
# Written on the 12th of March, 2017 as part of our graduation project, Clacket, which uses (and expands) 
# the Netflix Prize Dataset to build a recommendation engine.
# github: @blaringsilence

import requests
import time
import argparse
from pathlib import Path
from requests.exceptions import Timeout

def expand(start, file_path, encoding, o_success, o_failed):
	url = 'http://www.omdbapi.com/'
	with open(file_path, encoding=encoding) as movies:
		for index, line in enumerate(movies):
			if index + 1 >= start:
				try:
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
						with open(o_success, 'a') as expanded:
							expanded.write(expanded_info + '\n')
					except: # if not the movie, or the response isn't JSON/doesn't have the fields
						with open(o_failed, 'a') as couldnt:
							couldnt.write(line)
					start = index + 1
					print('\r' + str(start), end='', flush=True)
					time.sleep(2)
				except IndexError:
					print('There is an error in ' + file_path + '\'s format at line ' + str(index + 1) + ':'\
						  + '\nEvery line should have 3 comma-separated fields: id,year_of_release,title')
					break
				except Timeout: # if request times out
					time.sleep(30)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--start', help='Line number (starting from 1) of the first movie to fetch.',\
						type=int, default=1, metavar='')
	parser.add_argument('-f', '--file', help='Path for the file that contains'\
						+'the movie titles (every line is a movie in the following format: id,year_of_release,title',\
						type=str, default='movie_titles.txt', metavar='')
	parser.add_argument('-en', '--encoding', help='Encoding of input file: UTF-8 or ISO-8859-1.',\
						type=str, default='ISO-8859-1', choices=('UTF-8', 'ISO-8859-1'), metavar='')
	parser.add_argument('-exp', '--oexpanded', help='Path for the file where the expanded movies should be output (does not have to exist).',\
						type=str, default='expanded_movies.txt', metavar='')
	parser.add_argument('-fail', '--ofailed', help='Path for the file where the failed entries should be output (does not have to exist).',\
						type=str, default='couldnt_expand.txt', metavar='') 
	args = parser.parse_args()
	if Path(args.file).is_file():
		expand(args.start, args.file, args.encoding, args.oexpanded, args.ofailed)
	else:
		print('Please provide an existing input file.')