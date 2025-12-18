from src.processing import filter_by_state, sort_by_date


# Функция filter_by_state
def test_filter_by_state_executed(filter_by_state_executed):
    assert filter_by_state(filter_by_state_executed) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_filter_by_state_empty():
    assert filter_by_state([]) == []


def test_filter_by_state_canceled(filter_by_state_canceled):
    assert filter_by_state(filter_by_state_canceled, "CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}
    ]


def test_filter_by_state_executed_not_found(canceled):
    assert filter_by_state(canceled) == []


# Функция sort_by_date
def test_sort_by_date_reverse(date_list):
    assert sort_by_date(date_list) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date_not_reverse(date_list):
    assert sort_by_date(date_list, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_empty():
    assert sort_by_date([]) == []
