#!/usr/bin/env python3
from __future__ import print_function
import json
import sys
from loguru import logger


def dictor(data, path=None, default=None, checknone=False, ignorecase=False, pathsep=".", search=None, s2=None):
    '''
    Usage:
    get a value from a Dictionary key
    > dictor(data, "employees.John Doe.first_name")
    parse key index and fallback on default value if None,
    > dictor(data, "employees.5.first_name", "No employee found")
    pass a parameter
    > dictor(data, "company.{}.address".format(my_company))
    if using Python 3, can use F-strings to pass parameter
    > param = 'MyCompany'
    > dictor(data, f"company.{param}.address")
    lookup a 3rd element of List, on second key, lookup index=5
    > dictor(data, "3.first.second.5")
    lookup a nested list of lists
    > dictor(data, "0.first.1.2.second.third.0.2"
    check if return value is None, if it is, raise an error
    > dictor(data, "some.key.value", checknone=True)
    > ValueError: value not found for search path: "some.key.value"
    ignore letter casing when searching
    > dictor(data, "employees.Fred Flintstone", ignorecase=True)
    search data for specific keys (will return a list of all keys it finds)
    > dictor(data, "employees", search="name")
    '''

    logger.debug('0')
    if s2 is None and (path is None or path == ''):
        logger.debug('4')
        return data
           
    try:
        if path:
            for key in path.split(pathsep):
                if isinstance(data, (list, tuple)):    
                    val = data[int(key)]
                else:
                    if ignorecase:
                        for datakey in data.keys():
                            if datakey.lower() == key.lower():
                                key = datakey
                                break
                    val = data[key]
                data = val
            
        logger.debug('3')
        if search:
            search_ret = []     
            logger.debug('2')          
            if isinstance(data, (list, tuple)):
                logger.debug('list')
                for d in data:
                    for key in d.keys():
                        logger.warning(d.keys())
                        if key == search:
                            try:
                                search_ret.append(d[key])
                            except (KeyError, ValueError, IndexError, TypeError, AttributeError):
                                pass	    
            else:
                logger.debug(6)
                for key in data.keys():
                    logger.debug(data.keys())
                    if key == search:
                        try:
                            search_ret.append(data[key])
                        except (KeyError, ValueError, IndexError, TypeError, AttributeError):
                            pass
            if search_ret: 
                val = search_ret
            else:
                val = default
    except (KeyError, ValueError, IndexError, TypeError, AttributeError):
        val = default
            
    if s2:
        logger.error('8')
        logger.error(data)
        if s2 in data:
            logger.error('contains')
            val = 'contains!'
    if checknone:
        if val is None or val == default:
            raise ValueError('value not found for search path: "%s"' % path)
    return val


with open('tests/list.json') as data:
    a = json.load(data)

d = {
    "planets": [
        {
            "name": "Mars",
            "type": "rock",
            "attributes": {
                "name": "named after Roman god of war",
                "color": "red",
                "size" : "28,230 km"
            }
        },
        {
            "name": "Neptune",
            "type": "gas",
            "attributes": {
                "name": "named after Roman god of ocean",
                "color": "blue",
                "size" : "338,382 km"
            }
        },
    ]
}


#print(dictor(d, dictor(d, 'planets', search='attributes'),  search="size", default="couldnt find value"))
print(dictor(d, 'planets', s2='size'))