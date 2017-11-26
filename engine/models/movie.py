import pickle

import pandas as pd

from engine.models.feature import Feature


class Movie(object):
    features = [
        {'name': 'id', 'type': 'id'},
        {'name': 'title', 'type': 'id'},
        {'name': 'year', 'type': 'num'},
        {'name': 'genres', 'type': 'cat', 'list': True},
        {'name': 'actors', 'type': 'cat', 'list': True},
        {'name': 'directors', 'type': 'cat', 'list': True},
        {'name': 'writers', 'type': 'cat', 'list': True},
        {'name': 'languages', 'type': 'cat', 'list': True},
        {'name': 'countries', 'type': 'cat', 'list': True},
        {'name': 'type', 'type': 'cat'}
    ]

    ratings = None

    distances = pd.DataFrame(columns=['movie_id', 'distance'])

    def __init__(self, string):
        values = string.split('|')
        for index, feature in enumerate(self.features):
            feature['value'] = values[index]
            f = Feature(**feature)
            setattr(self, feature['name'], f)

    def __str__(self):
        return str([getattr(self, f['name']).value for f in self.features])

    def __sub__(self, other):
        # 1. Numerical
        numerical = [
            getattr(self, f['name']) - getattr(other, f['name'])
            for f in self.features if f['type'] == 'num']
        distance_num = sum(numerical)
        # ^ would need to be adjusted if we add more numerical features

        # 2. Categorical
        categorical = [
            getattr(self, f['name']) - getattr(other, f['name'])
            for f in self.features if f['type'] == 'cat']
        cat_intersect = sum([x['intersect'] for x in categorical])
        cat_only_self = sum([x['only_self'] for x in categorical])
        cat_only_other = sum([x['only_other'] for x in categorical])
        cat_similarity = cat_intersect / (cat_intersect +
                                          cat_only_other +
                                          cat_only_self)
        distance_cat = 1 - cat_similarity

        return distance_num + distance_cat

    def add_distance(self, other, switch=True):
        if not (self.distances['movie_id'] == other.id.value).any() \
                and other.id != self.id:
            distance = self - other
            self.distances = self.distances.append(
                {'movie_id': other.id.value, 'distance': distance},
                ignore_index=True)
        if switch:
            other.add_distance(self, switch=False)

    def save(self, folder):
        with open('{0}/mv_{1}.pyc'.format(folder, self.id.value), 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, folder, id):
        with open('{0}/mv_{1}.pyc'.format(folder, id), 'rb') as f:
            movie = pickle.load(f)
        return movie
