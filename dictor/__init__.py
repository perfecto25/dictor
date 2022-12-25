#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import json


def _pretty(data, pretty):
    """return output in pretty print"""
    if pretty:
        return json.dumps(data, indent=4, sort_keys=True)
    else:
        return data


def _search(data, search, default):
    """search for specific keys"""
    search_ret = []
    if isinstance(data, (list, tuple)):
        for d in data:
            for key in d.keys():
                if key == search:
                    try:
                        search_ret.append(d[key])
                    except (KeyError, ValueError, IndexError, TypeError, AttributeError):
                        pass
    else:
        for key in data.keys():
            if key == search:
                try:
                    search_ret.append(data[key])
                except (KeyError, ValueError, IndexError, TypeError, AttributeError):
                    pass
    if search_ret:
        val = search_ret
    else:
        val = default
    return val


def _findval(data, path, pathsep, ignorecase):
    """cycle through Dict and find the key's value"""
    if r"\." in path:
        path = path.replace(r"\.", "__dictor__")

    for key in path.split(pathsep):
        if "__dictor__" in key:
            key = key.replace("__dictor__", ".")
        if isinstance(data, (list, tuple)):
            try:
                val = data[int(key)]
            except (UnboundLocalError, IndexError, ValueError):
                val = None
        else:
            if ignorecase:
                for datakey in data.keys():
                    if datakey.lower() == key.lower():
                        key = datakey
                        break
            try:
                if data and key in data:
                    val = data[key]
                else:
                    val = None
                    break
            except TypeError:
                val = None
        data = val
    return val


def dictor(
    data,
    path=None,
    default=None,
    checknone=False,
    ignorecase=False,
    pathsep=".",
    search=None,
    pretty=False,
    rtype=None,
):
    """Get a value or a list of values from a dictionary key using a path

    Args:
        data (dict): Input dictionary to be searched in.
        path (str, optional): Dictionary key search path (pathsep separated).
            Defaults to None.
        default (Any, optional): Default value to return if the key is not found.
            Defaults to None.
        checknone (bool, optional): If set, an exception is thrown if the value
            is None. Defaults to False.
        ignorecase (bool, optional): If set, upper/lower-case keys are treated
            the same. Defaults to False.
        pathsep (str, optional): Path separator for path parameter. Defaults to ".".
        search (Any, optional): Search for specific keys and output a list of values.
            Defaults to None.
        pretty (bool, optional): Pretty prints the result. Defaults to False.

    Raises:
        ValueError: Raises if checknone is set.

    Returns:
        Any: Returns one value or a list of values for the specified key.

    Examples:
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
        pretty-print output
        > dictor(data, "employees", pretty=True)
        return a value in a specific type format
        > dictor(data, "employee_id", rtype="int")
    """

    ## return entire JSON if no search path specified
    if all([search is None, path is None]):
        return _pretty(data, pretty)

    val = None

    if path:
        val = _findval(data, path, pathsep, ignorecase)
    if search and path and val:
        val = _search(val, search, default)
    if search and not path:
        val = _search(data, search, default)

    if checknone:
        if val is None or val == default:
            raise ValueError('value not found for search path: "%s"' % path)

    if val is None or val == "":
        return default

    # return specific type
    if rtype and (type(val) is str or type(val) is int):
        try:
            if rtype == "int":
                val = int(val)
            if rtype == "str":
                val = str(val)
        except ValueError:
            pass
    return _pretty(val, pretty)
