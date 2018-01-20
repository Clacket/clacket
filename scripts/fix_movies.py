import pandas as pd

from engine.models.movie import Movie


DATASET = 'dataset/expanded_movies.txt'
TRAINING = 'dataset/training_set'


def save_all(folder, li):
    with open(DATASET) as dataset:
        for movie_line in dataset:
            if movie_line.split('|')[0] in li:
                movie_line = movie_line.rstrip('\n')
                movie = Movie(movie_line)
                movie.save(folder)


def add_all_ratings(folder, li):
    with open(DATASET) as dataset:
        for movie_line in dataset:
            movie_id = movie_line.split('|')[0]
            if movie_id in li:
                movie = Movie.load(folder, movie_id)
                zeros = '0' * (7 - len(movie_id))
                ratings_file = '{0}/mv_{1}{2}.txt'.format(
                    TRAINING, zeros, movie_id)
                ratings_df = pd.read_csv(
                    ratings_file,
                    header=None,
                    names=['user_id', 'rating', 'date'],
                    skiprows=1,
                    parse_dates=['date'],
                    infer_datetime_format=True)
                movie.ratings = ratings_df
                movie.save(folder)


if __name__ == '__main__':
    folder = '/media/mariam/Files/ran/clacket-save'
    li = []
    with open(DATASET) as dataset:
        for movie_line in dataset:
            movie_id = movie_line.split('|')[0]
            try:
                m = Movie.load(folder, movie_id)
            except EOFError:
                li.append(movie_id)
    print('Found {0} movies in need of fixing...'.format(len(li)))
    print(str(li))
    print("Saving...")
    save_all(folder, li)
    print("Adding ratings...")
    add_all_ratings(folder, li)
