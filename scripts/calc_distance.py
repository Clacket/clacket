import sys

from engine.models.movie import Movie
from engine.models.distance import DistanceMatrix


DATASET = 'dataset/expanded_movies.txt'


def calc_distance(movie_id, folder, matrix):
    movie = Movie.load(folder, movie_id)
    with open(DATASET) as dataset:
        for movie_line in dataset:
            temp_id = movie_line.split('|')[0]
            if int(temp_id) > int(movie.id.value):
                temp_string = movie_line.rstrip('\n')
                temp = Movie(temp_string)
                distance = movie - temp
                matrix.update(movie.id.value, temp_id, distance)


def calc_all(folder):
    matrix = DistanceMatrix(folder)
    with open(DATASET) as dataset:
        movie_ids = [m.split('|')[0] for m in dataset]
    for i, movie_id in enumerate(movie_ids):
        calc_distance(movie_id, folder, matrix)
        percentage = (i / 9399) * 100
        sys.stdout.write(
            "\rProgress: {0}% ({1} out of 9399)"
            .format(percentage, i))
        sys.stdout.flush()
    print("\nSaving distance matrix...")
    matrix.save()


def calc_one(movie_id, folder):
    # Assumes existing distance matrix
    matrix = DistanceMatrix(folder)
    matrix.load()
    calc_distance(movie_id, folder, matrix)
    # here: also add the movie to the dataset
    matrix.save()


if __name__ == '__main__':
    folder = '/media/mariam/Files/ran/clacket-save'
    calc_all(folder)
