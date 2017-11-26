from engine.models.movie import Movie


DATASET = 'dataset/expanded_movies.txt'


def calc_distance(movie_id, folder):
    movie = Movie.load(folder, movie_id)
    with open(DATASET) as dataset:
        for movie_line in dataset:
            temp_id = movie_line.split('|')[0]
            temp = Movie.load(folder, temp_id)
            movie.add_distance(other=temp)
            temp.save(folder)
    movie.save(folder)


def calc_all(folder):
    with open(DATASET) as dataset:
        for movie_line in dataset:
            movie_id = movie_line.split('|')[0]
            calc_distance(movie_id, folder)


if __name__ == '__main__':
    folder = '/media/mariam/Files/ran/clacket-save'
    calc_all(folder)
