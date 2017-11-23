from engine.models.movie import Movie


DATASET = '../dataset/expanded_movies.txt'


def parse(string):
    return Movie(string)


if __name__ == '__main__':
    string = "1|Dinosaur Planet|2003|"\
             "Documentary,Animation,Family|"\
             "Christian Slater,Scott Sampson|"\
             "N/A|N/A|English|USA|series"
    movie = parse(string)
    string2 = "20|Seeta Aur Geeta|1972|"\
              "Comedy,Drama,Family|"\
              "Dharmendra,Sanjeev Kumar,Hema Malini,Manorama|"\
              "Ramesh Sippy|Javed Akhtar,Javed Akhtar,"\
              "Satish Bhatnagar,Satish Bhatnagar,"\
              "Salim Khan,Salim Khan|Hindi|India|movie"
    movie2 = parse(string2)

    print(movie)
    print(movie2)
    print(movie - movie2)
