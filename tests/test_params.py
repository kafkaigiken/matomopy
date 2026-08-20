"""Unit tests for the parameter-encoding helpers."""

from matomopy.params import encode_params


def test_scalars_and_aliases():
    pairs = encode_params({"id_site": 1, "period": "day"})
    assert ("idSite", "1") in pairs
    assert ("period", "day") in pairs


def test_none_values_are_dropped():
    pairs = encode_params({"idSite": 1, "segment": None})
    assert pairs == [("idSite", "1")]


def test_booleans_become_one_or_zero():
    pairs = dict(encode_params({"flat": True, "expanded": False}))
    assert pairs["flat"] == "1"
    assert pairs["expanded"] == "0"


def test_flat_list_is_comma_joined():
    pairs = dict(encode_params({"idSites": [1, 2, 3]}))
    assert pairs["idSites"] == "1,2,3"


def test_empty_sequence_is_dropped():
    pairs = encode_params({"columns": [], "period": "day"})
    assert pairs == [("period", "day")]


def test_dict_becomes_bracketed():
    pairs = dict(encode_params({"filter": {"a": 1, "b": 2}}))
    assert pairs["filter[a]"] == "1"
    assert pairs["filter[b]"] == "2"


def test_nested_list_uses_indexed_brackets():
    pairs = dict(encode_params({"urls": [{"a": 1}, {"a": 2}]}))
    assert pairs["urls[0][a]"] == "1"
    assert pairs["urls[1][a]"] == "2"
