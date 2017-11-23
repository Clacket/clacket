import copy

import pytest

from engine.models.feature import Feature


@pytest.fixture
def numeric_kwargs():
    return {  # strictly non-list
        'name': 'numeric_feature',
        'type': 'num',
        'value': '210323'
    }


@pytest.fixture
def non_numeric_kwargs():
    return {  # strictly non-list
        'name': 'non_numeric_feature',
        'type': 'cat',
        'value': '22323'
    }


@pytest.fixture
def non_numeric_list_kwargs():
    return {  # strictly 3 items in the list (1, 2, 3)
        'name': 'non_numeric_list',
        'type': 'cat',
        'value': '1,2,3',
        'list': True
    }


@pytest.fixture
def non_numeric_feature(non_numeric_kwargs):
    return Feature(**non_numeric_kwargs)


@pytest.fixture
def numeric_feature(numeric_kwargs):
    return Feature(**numeric_kwargs)


@pytest.fixture
def non_numeric_list_feature(non_numeric_list_kwargs):
    return Feature(**non_numeric_list_kwargs)


def test_init_numeric(numeric_feature, numeric_kwargs):
    assert numeric_feature.name == numeric_kwargs['name']
    assert numeric_feature.type == numeric_kwargs['type']
    assert numeric_feature.value == int(numeric_kwargs['value'])
    assert str(numeric_feature) == numeric_kwargs['value']
    assert not numeric_feature.is_list


def test_numeric_list_init(numeric_kwargs):
    list_numeric_kwargs = copy.copy(numeric_kwargs)
    list_numeric_kwargs['list'] = True
    with pytest.raises(ValueError) as exc:
        Feature(**list_numeric_kwargs)
    assert 'Numerical values cannot be lists' in exc.value.args[0]


def test_init_non_numeric(non_numeric_feature, non_numeric_kwargs):
    assert non_numeric_feature.value == non_numeric_kwargs['value']
    assert str(non_numeric_feature) == non_numeric_feature.value


def test_self_distance(
        numeric_feature, non_numeric_feature, non_numeric_list_feature):
    assert (numeric_feature - numeric_feature) == 0

    with pytest.raises(ValueError) as exc:
        numeric_feature - non_numeric_feature
    assert 'features must have the same name & type' in exc.value.args[0]

    with pytest.raises(ValueError) as exc2:
        non_numeric_feature - non_numeric_list_feature
    assert 'features must have the same name & type' in exc2.value.args[0]

    difference = non_numeric_feature - non_numeric_feature
    assert difference['intersect'] == 1
    assert difference['only_self'] == 0
    assert difference['only_other'] == 0

    difference_list = non_numeric_list_feature - non_numeric_list_feature
    assert difference_list['intersect'] == 3
    assert difference_list['only_self'] == 0
    assert difference_list['only_other'] == 0


def test_shuffled_list_distance(
        non_numeric_list_feature, non_numeric_list_kwargs):
    shuffled_kwargs = copy.copy(non_numeric_list_kwargs)
    shuffled_kwargs['value'] = '2,3,1'
    shuffled_feature = Feature(**shuffled_kwargs)
    difference = non_numeric_list_feature - shuffled_feature
    assert difference['intersect'] == 3
    assert difference['only_self'] == 0
    assert difference['only_other'] == 0


def test_missing_value_distance(numeric_feature, numeric_kwargs):
    missing_kwargs = copy.copy(numeric_kwargs)
    missing_kwargs['value'] = 'N/A'
    missing_feature = Feature(**missing_kwargs)
    assert missing_feature.value is None
    assert numeric_feature.value is not None
    assert (missing_feature - numeric_feature) == 1  # max difference
