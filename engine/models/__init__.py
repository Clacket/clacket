class Feature(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.is_list = kwargs.get('list', False)
        self.value = kwargs.get('value', '').split(',') if self.is_list \
            else kwargs.get('value')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        vals = [val] if not self.is_list else val
        processed = []
        for value in vals:
            if value != 'N/A':
                formatted = value.lower() if not self.type == 'num' \
                            else int(value)
                processed.append(formatted)
        if len(processed) == 0:
            self._value = None
        elif self.is_list:
            self._value = processed
        else:
            self._value = processed[0]

    def __str__(self):
        return str(self.value)

    def __sub__(self, other):
        # 1. Only allow valid subtractions
        if self.name != other.name or self.type != other.type:
            raise ValueError('Both features must have the same name & type.')

        # 2. Numerical (Eucledian)
        if self.type == 'num':
            if self.value is None or other.value is None:
                similarity = 0
            else:
                similarity = 1 / (1 + abs(self.value - other.value))
            return 1 - similarity

        # 3. Categorical
        # Do not compare if one of them is N/A (make as far as possible)
        if self.value is None or other.value is None:
            intersect, only_self, only_other = 0, 0, 0
        elif self.is_list:
            intersect = len([x for x in self.value if x in other.value])
            only_self = len([x for x in self.value if x not in other.value])
            only_other = len([x for x in other.value if x not in self.value])
        else:
            if self.value == other.value:
                intersect, only_self, only_other = 1, 0, 0
            else:
                intersect, only_self, only_other = 0, 1, 1
        return dict(
            intersect=intersect, only_other=only_other, only_self=only_self)


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
