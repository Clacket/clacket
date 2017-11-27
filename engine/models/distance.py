import pickle


class DistanceMatrix(object):
    def __init__(self, folder):
        self.matrix = {}
        self.filename = '{0}/distances.pyc'.format(folder)

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.matrix, file)

    def load(self):
        with open(self.filename, 'rb') as file:
            self.matrix = pickle.load(file)

    def get(self, id1, id2):
        id1, id2 = int(id1), int(id2)
        if id1 == id2:
            return 0
        else:
            smaller = min(id1, id2)
            bigger = max(id1, id2)
            return self.matrix[smaller][bigger]

    def update(self, id1, id2, distance):
        smaller = min(id1, id2)
        bigger = max(id1, id2)
        if smaller not in self.matrix:
            self.matrix[smaller] = {}
        self.matrix[smaller][bigger] = distance
