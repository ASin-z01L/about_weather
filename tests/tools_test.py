import pytest
import app.tools as tool
from datetime import date


# date_to_str
@pytest.mark.parametrize("date_obj, date_format, result", [
    (date(2026, 1, 1), "%Y-%m-%d", "2026-01-01"),
    (date(2026, 12, 31), "%d/%m/%Y", "31/12/2026"),
    (date(2026, 5, 9), "%B %d, %Y", "May 09, 2026"),
    (date(2026, 7, 4), "%a, %d %b %Y", "Sat, 04 Jul 2026"),
])
def test_date_to_str_formats(date_obj, date_format, result):
    assert tool.date_to_str(date_obj, date_format) == result


def test_date_to_str_basic():
    assert tool.date_to_str(date(2026, 3, 18)) == '2026-03-18'


# str_to_date
@pytest.mark.parametrize("date_str, date_format, result", [
    ("2026-01-01", "%Y-%m-%d", date(2026, 1, 1)),
    ("31/12/2026", "%d/%m/%Y", date(2026, 12, 31)),
    ("May 09, 2026", "%B %d, %Y", date(2026, 5, 9)),
    ("Sat, 04 Jul 2026", "%a, %d %b %Y", date(2026, 7, 4)),
])
def test_str_to_date_formats(date_str, date_format, result):
    assert tool.str_to_date(date_str, date_format) == result


def test_str_to_date_basic():
    assert tool.str_to_date('2026-03-18') == date(2026, 3, 18)


# trim_json
@pytest.mark.parametrize('str_json, result', [
    ('begin trash [{"city":"London","dates":["2026-03-02"]}] end trash', '[{"city":"London","dates":["2026-03-02"]}]'),
    ('begin trash {"city":"London","dates":["2026-03-02"]} end trash', '{"city":"London","dates":["2026-03-02"]}'),
    ('[{"city":"London","dates":["2026-03-02"]}]', '[{"city":"London","dates":["2026-03-02"]}]'),
    ('{"city":"London","dates":["2026-03-02"]}', '{"city":"London","dates":["2026-03-02"]}'),
])
def test_trim_json_basic(str_json, result):
    assert tool.trim_json(str_json) == result


# trim_context
def test_trim_context_basic():
    list_for_trim = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    assert tool.trim_context(list_for_trim) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def test_trim_context_with_max_size():
    list_for_trim = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    assert tool.trim_context(list_for_trim, 3) == [9, 10, 11]
