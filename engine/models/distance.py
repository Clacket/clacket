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
            smaller = str(min(id1, id2))
            bigger = str(max(id1, id2))
            return self.matrix[smaller][bigger]

    def get_all(self, id):
        min_id = min(self.matrix.keys())
        all_ids = [min_id] + list(self.matrix[min_id].keys())
        return self.get_some(id, all_ids)

    def get_some(self, id, ids):
        distances = []
        for id2 in ids:
            distances.append((id2, self.get(id, id2)))
        return distances

    def update(self, id1, id2, distance):
        smaller = min(id1, id2)
        bigger = max(id1, id2)
        if smaller not in self.matrix:
            self.matrix[smaller] = {}
        self.matrix[smaller][bigger] = distance
