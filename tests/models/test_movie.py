import copy

import pytest

from engine.models.movie import Movie


@pytest.fixture
def valid_movie():
    string = "1|Dinosaur Planet|2003|"\
             "Documentary,Animation,Family|"\
             "Christian Slater,Scott Sampson|"\
             "N/A|N/A|English|USA|series"
    return Movie(string)


def test_distance_same_movie(valid_movie):
    assert (valid_movie - valid_movie) == 0


def test_distance_different_movie(valid_movie):
    different_movie = copy.deepcopy(valid_movie)
    different_movie.year.value = valid_movie.year.value + 20
    assert (valid_movie - different_movie) != 0


def test_parse(valid_movie):
    assert valid_movie.id == '1'
    assert valid_movie.title == 'dinosaur planet'
    assert valid_movie.genres == ['documentary', 'animation', 'family']
    assert valid_movie.actors == ['christian slater', 'scott sampson']
    assert valid_movie.directors.value is None
    assert valid_movie.writers.value is None
    assert valid_movie.languages == ['english']
    assert valid_movie.countries == ['usa']
    assert valid_movie.type == 'series'
