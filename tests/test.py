
#!/usr/bin/env python
# coding=utf-8
'''
DICTOR testing suite
shell> nosetest test.py
'''

from __future__ import print_function
import json
import sys
sys.path.append("..")
import nose
from nose.tools import eq_, raises
from dictor import dictor

with open('basic.json') as data:
    BASIC = json.load(data)

with open('list.json') as data:
    LIST = json.load(data)

with open('large.json') as data:
    LARGE = json.load(data)


def test_simple_list():
    ''' test for basic list value '''
    result = dictor(LIST, '1.name')
    eq_('gone with the wind', result)

def test_simple_dict():
    ''' test for value in a dictionary '''
    result = dictor(BASIC, 'robocop.year')
    eq_(1989, result)

def test_complex_dict():
    ''' test parsing down a list and getting dict value '''
    result = dictor(BASIC, 'terminator.1.terminator 2.genre.0')
    eq_('nuclear war', result)

def test_keys_with_dots():
    ''' test parsing keys with dots in them '''
    result = dictor(BASIC, 'dirty\.harry.genre')
    eq_('romance', result)

def test_ignore_letter_casing():
    ''' test ignoring letter upper/lower case '''
    result = dictor(BASIC, 'austin PoWeRs.year', ignorecase=True)
    eq_(1996, result)

def test_parsing_large_JSON():
    ''' test parsing large JSON file '''
    
    result = dictor(LARGE, '0.tags.3')
    eq_('sunt', result)

    result = dictor(LARGE, '1.friends.2.name')
    eq_('Tanisha Saunders', result)

@raises(ValueError)
def test_exception():
    ''' test for non existent index value '''
    dictor(LIST, '5.genre', checknone=True)

if __name__ == "__main__":
    nose.run()
