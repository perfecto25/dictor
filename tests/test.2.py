
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

from dictor import dictor

with open('basic.json') as data:
    basicfile = json.load(data)

with open('list.json') as data:
    listfile = json.load(data)

with open('complex.json') as data:
    complexfile = json.load(data)


with open('spaceballs.json') as data:
    spaceballs = json.load(data)


print(dictor(listfile, '0.message'))

#print(dictor(basicfile, '1.genre'))
#print(dictor(spaceballs, 'characters.Dark Helmet.items.0'))