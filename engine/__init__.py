from engine.models import Movie


DATASET = '../dataset/expanded_movies.txt'


def parse(string):
    return Movie(string)


if __name__ == '__main__':
    string = "1|Dinosaur Planet|2003|"\
             "Documentary,Animation,Family|"\
             "Christian Slater,Scott Sampson|"\
             "N/A|N/A|English|USA|series"
    movie = parse(string)
    print(movie)
