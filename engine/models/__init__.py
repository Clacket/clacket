class Feature(object):
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.is_list = kwargs.get('list', False)
        if self.is_list:
            self.value = kwargs.get('value', '').split(',')

        else:
            self.value = kwargs.get('value')

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
