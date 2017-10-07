from ..paneltools import *
import pytest


@pytest.fixture
def empty_panels():
    return []


@pytest.fixture
def one_panel():
    return [{'col': 1, 'row': 1, 'size_x': 2, 'size_y': 2}]


@pytest.fixture
def many_panels():
    return [
        {'col': 6, 'row': 1, 'size_x': 2, 'size_y': 1},
        {'col': 4, 'row': 2, 'size_x': 3, 'size_y': 1},
        {'col': 6, 'row': 3, 'size_x': 2, 'size_y': 1},
        {'col': 1, 'row': 1, 'size_x': 2, 'size_y': 1},
        {'col': 3, 'row': 1, 'size_x': 1, 'size_y': 2},
        {'col': 4, 'row': 1, 'size_x': 1, 'size_y': 1}
    ]


def test_empty_bottoms(empty_panels):
    assert not bottoms(empty_panels)


def test_one_panel_bottoms(one_panel):
    lines = bottoms(one_panel)
    assert len(lines) == 1
    assert lines[0][2] == 3 # col2
    assert lines[0][3] == 3 # row2


def test_many_panels_bottoms(many_panels):
    lines = bottoms(many_panels)
    assert len(lines) == len(many_panels)


def test_find_shape_empty(empty_panels):
    assert len(find_shape(bottoms(empty_panels), 8)) == 8


def test_find_shape(one_panel):
    shape = find_shape(bottoms(one_panel), 8)
    assert shape[0] == 3
    assert shape[1] == 3
    assert shape[2] == 1


def test_find_shape_many(many_panels):
    shape = find_shape(bottoms(many_panels), 7)
    assert shape == [2, 2, 3, 3, 3, 4, 4]


def test_longest_lines(empty_panels):
    shape = find_shape(bottoms(empty_panels), 8)
    assert len(longest_lines(shape)) == 1


def test_longest_lines_one(one_panel):
    lines = longest_lines(find_shape(bottoms(one_panel), 8))
    assert len(lines) == 2
    assert lines[0] == {'col': 3, 'len': 6, 'row': 1}
    assert lines[1] == {'col': 1, 'len': 8, 'row': 3}


def test_find_place(one_panel):
    lines = longest_lines(find_shape(bottoms(one_panel), 8))

    place = find_place(lines, 6)
    assert place == {'col': 3, 'row': 1, 'len': 6}

    place = find_place(lines, 7)
    assert place == {'col': 1, 'row': 3, 'len': 8}


