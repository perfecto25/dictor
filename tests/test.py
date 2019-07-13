
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


def test_simple_list():
    ''' test for basic list value '''
    result = dictor(LIST, '1.genre')
    eq_('documentary', result)

def test_simple_dict():
    ''' test for value in a dictionary '''
    result = dictor(BASIC, 'robocop.year')
    eq_(1989, result)

def test_complex_dict():
    ''' test parsing down a list and getting dict value '''
    result = dictor(BASIC, 'terminator.1.terminator 2.genre.0')
    eq_('nuclear war', result)

@raises(ValueError)
def test_exception():
    ''' test for non existent index value '''
    dictor(LIST, '5.genre', checknone=True)

if __name__ == "__main__":
    nose.run()
