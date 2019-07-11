
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

with open('basic.json') as data:
    BASIC = json.load(data)

with open('list.json') as data:
    LIST = json.load(data)



def dictor(data, path=None, default=None, checknone=False):
    '''
    Usage:
    get a value from a Dictionary key
    > dictor(data, "employees.John Doe.first_name")

    parse key index and fallback on default value if None,
    > dictor(data, "employees[5].first_name", default="No employee found")

    pass a parameter
    > dictor(data, "company.name.{}".format(my_company))

    lookup a 3rd element of List, on second key, lookup index=5
    > dictor(data, "3.first.second[5]")

    lookup a nested list of lists
    > dictor(data, "0.first[1].2.second.third[0].2"

    check if return value is None, if it is, raise an error
    > dictor(data, "some.key.value", checknone=True)
    > ValueError: missing value for ['some']['key']['value']
    '''

    import json
    import sys
    # import Reduce if py3
    if sys.version_info[0] == 3:
        from functools import reduce

    if path is None or path == '':
        return json.dumps(data)

    value = None
    keys = path.split(".")

    # reset path
    path = None

    # if 1st key is a list index
    # if all(char.isdigit() for char in keys[0]):
    #     path = '['+keys[0]+']'

    #     # remove 1st key from key list
    #     keys.pop(0)
    # print(keys)

    # if JSON is a list objects
    if isinstance(data, list):
        if keys[0].isdigit():
            print('isdigit')
            position = int(keys[0])
        
            #try: 
            #    data = data[position]
             
    #         except (KeyError, ValueError, IndexError, TypeError) as err:
    #             value = default
    #print(default)

    # build proper path
    # for key in keys:
    #     # check if key is a list
    #     if key.endswith(']'):
    #         temp = key.split('[')
    #         key = ''.join(temp[0])
    #         index = int(temp[1].strip(']'))
    #         if path is None:
    #             path = "['"+key+"']"+"["+str(index)+"]"
    #         else:
    #             path = path+"['"+key+"']"+"["+str(index)+"]"
    #     else:
    #         if path is None:
    #             path = "['"+key+"']"

    #         else:
    #             # check if key is an index
    #             if key.isdigit() is True:
    #                 path = path + "["+key+"]"
    #             else:
    #                 path = path + "['"+key+"']"
    # print(path)
    print(keys)
    for i in range(len(keys)):
        print(i)
        key = keys[i]
        print('key: ' + key)
        try:
            val = data[key]
            data = val
            print('data: ' + str(data))
        except (KeyError, ValueError, IndexError, TypeError) as err:
            return default
        
    # for key in keys:
    #     try:
    #         print('data'+key)
    #         val = data[key]
    #         print('==' + val)
    #     except (KeyError, ValueError, IndexError, TypeError) as err:
    #         return 'none2'
        
    # try:
    #     print(keys)
    #     for key in keys:

    #     value = reduce(lambda c, k: c.get(k, {}), keys, data)
    #     #value = reduce(dict.get, data, path)
        
    #     print('----')
    #     print(value)
    # except (KeyError, ValueError, IndexError, TypeError) as err:
    #     value = default
    # finally:
    #     if checknone:
    #         if not value:
    #             raise ValueError('missing value for %s' % path)
    #     if bool(value) is False or value is None:
    #         value = default
    #     return value

print(dictor(BASIC, 'robocop.actors.2'))

#print(dictor(LIST, '2.name'))