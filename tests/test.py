#!/usr/bin/env python
# coding=utf-8
"""
DICTOR testing suite
shell> pytest test.py
"""

from __future__ import print_function
import json
import sys
import pytest
from os.path import dirname, join, abspath

## import repo version of dictor, not pip-installed version
sys.path.insert(0, abspath(join(dirname(__file__), "..")))
from dictor import dictor

with open("basic.json") as data:
    BASIC = json.load(data)

with open("list.json") as data:
    LIST = json.load(data)

with open("large.json") as data:
    LARGE = json.load(data)

def test_simple_list():
    """test for basic list value"""
    result = dictor(LIST, "1.name")
    assert result == "gone with the wind"

def test_simple_dict():
    """test for value in a dictionary"""
    result = dictor(BASIC, "robocop.year")
    assert result == 1989

def test_non_existent_value():
    """test a non existent key search"""
    result = dictor(BASIC, "non.existent.value")
    assert result is None

    result = dictor({"lastname": "Doe"}, "foo.lastname")
    assert result is None

def test_zero_value():
    """test a Zero value - should return 0"""
    result = dictor(BASIC, "terminator.2.terminator 3.year", checknone=True)
    assert result == 0

def test_partial_exist_value():
    """partially existing value"""
    result = dictor(BASIC, "spaceballs.year.fakekey")
    assert result is None

def test_random_chars():
    result = dictor(BASIC, "#.random,,,@.chars")
    assert result == '({%^&$"'

def test_complex_dict():
    """test parsing down a list and getting dict value"""
    result = dictor(BASIC, "terminator.1.terminator 2.genre.0")
    assert result == "nuclear war"

def test_pathsep():
    """test parsing down a list and getting dict value with pathsep"""
    result = dictor(BASIC, "terminator/1/terminator 2/genre/0", pathsep="/")
    assert result == "nuclear war"

def test_keys_with_different_pathsep():
    """test parsing keys with different path separator"""
    result = dictor(BASIC, "dirty.harry/genre", pathsep="/")
    assert result == "romance"

def test_escape_pathsep():
    """test using escape path separator"""
    result = dictor(BASIC, "dirty\.harry.genre")
    assert result == "romance"

def test_ignore_letter_casing():
    """test ignoring letter upper/lower case"""
    result = dictor(BASIC, "austin PoWeRs.year", ignorecase=True)
    assert result == 1996

def test_ignore_letter_casing_nested():
    """test ignoring letter upper/lower case"""
    result = dictor(BASIC, "austin PoWeRs.Year", ignorecase=True)
    assert result == 1996

def test_numeric_key_handling():
    """test handling keys that are numbers"""
    result = dictor(BASIC, "1492.year")
    assert result == 1986

def test_parsing_large_JSON():
    """test parsing large JSON file"""
    result = dictor(LARGE, "0.tags.3")
    assert result == "sunt"

    result = dictor(LARGE, "1.friends.2.name")
    assert result == "Tanisha Saunders"

def test_parsing_large_JSON_nonexistent():
    """test parsing large JSON file w nonexistent value"""
    result = dictor(LARGE, "some.value")
    assert result is None

def test_exception():
    """test for non existent index value"""
    with pytest.raises(ValueError):
        dictor(LIST, "5.genre", checknone=True)

def test_searching_list_JSON():
    """test searching list JSON file"""
    result = dictor(LIST, search="name")
    assert result == ["spaceballs", "gone with the wind", "titanic"]

def test_searching_large_JSON():
    """test searching large JSON file"""
    result = dictor(LARGE, "0.friends", search="name")
    assert result == ["Patsy Sargent", "Bailey Carpenter", "Corina Sherman"]

def test_return_type_int():
    """test returning int type"""
    result = dictor(BASIC, "conan the barbarian.year", rtype="int")
    assert result == 1983

def test_return_type_str():
    """test returning str type"""
    result = dictor(BASIC, "spaceballs.year", rtype="str")
    assert result == "1987"

def test_return_invalid_rtype():
    """test string to int invalid rtype"""
    result = dictor(BASIC, "spaceballs.genre", rtype="int")
    assert result == "comedy"

def test_empty_string_path():
    """test empty string path"""
    result = dictor(BASIC, "")
    assert result is None

def test_malformed_search_path():
    """test_malformed_search_path"""
    result = dictor(BASIC, "spaceballs.")
    assert result is None

def test_non_existent_path_search():
    """test_non_existent_path_search"""
    result = dictor(BASIC, "nonexistent.subkey", search="abc")
    assert result is None

    result = dictor(BASIC, "nonexistent.subkey", default="path doesnt exist", search="abc")
    assert result == "path doesnt exist"