class Feature(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.is_list = kwargs.get('list', False)
        if self.is_list and self.type == 'num':
            raise ValueError('Numerical values cannot be lists.')
        self.value = kwargs.get('value', 'N/A')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        vals = [val] if not self.is_list else val.split(',')
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

    def __eq__(self, other):
        return self.value == other.value if isinstance(other, Feature) \
            else self.value == other

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
            only_self = len(self.value) - intersect
            only_other = len(other.value) - intersect
        else:
            if self.value == other.value:
                intersect, only_self, only_other = 1, 0, 0
            else:
                intersect, only_self, only_other = 0, 1, 1
        return dict(
            intersect=intersect, only_other=only_other, only_self=only_self)
