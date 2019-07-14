# Dictor - the dictionary doctor
## An elegant dictionary and JSON handler

Version 0.1.1

Dictor is a Python 2 and 3 compatible JSON/Dictionary handler.

Dictor takes a dictionary or JSON data and returns value for a specific key.

If Dictor doesnt find a value for a key, or if JSON or Dictionary data is missing the key, the return value is either None or whatever fallback value you provide.

Dictor is polite with Exception errors commonly encountered when parsing large Dictionaries/JSONs. 

Using Dictor eliminates the repeated use of try/except blocks in your code when dealing with lookups of large JSON structures, as well as providing flexibility for inserting fallback values on missing keys/values.



---

## Installation
```
pip install dictor
```

## Usage


sample.json

```
{
    "characters": {
        "Lonestar": {
            "id": 55923,
            "role": "renegade",
            "items": [
                "space winnebago",
                "leather jacket"
            ]
        },
        "Barfolomew": {
            "id": 55924,
            "role": "mawg",
            "items": [
                "peanut butter jar",
                "waggy tail"
            ]
        },
        "Dark Helmet": {
            "id": 99999,
            "role": "Good is dumb",
            "items": [
                "Shwartz",
                "helmet"
            ]
        },
        "Skroob": {
            "id": 12345,
            "role": "Spaceballs CEO",
            "items": [
                "luggage"
            ]
        }
    }
}
```

now lets get info on all Characters
```
from dictor import dictor

with open('sample.json') as data: 
    data = json.load(data)

print(dictor(data, 'characters'))

{u'Lonestar': {u'items': [u'space winnebago', u'leather jacket'], u'role': u'renegade', u'id': 55923}, u'Dark Helmet': {u'items': [u'Shwartz', u'helmet'], u'role': u'Good is dumb', u'id': 99999}, u'Barfolomew': {u'items': [u'peanut butter jar', u'waggy tail'], u'role': u'mawg', u'id': 55924}, u'Skroob': {u'items': [u'luggage'], u'role': u'Spaceballs CEO', u'id': 12345}}
```
---

get details for Dark Helmet
```
print(dictor(data, 'characters.Dark Helmet.items'))

[u'Shwartz', u'helmet']
```

you can also pass a flag to ignore letter Upper/Lower casing,
```
print(dictor(data, 'characters.dark helmet.items', ignorecase=True))
```

---

get only the 1st Item of a character
```
print(dictor(data, 'characters.Dark Helmet.items.0'))

Shwartz
```
---


## Fallback Value & Error Handling
by default, dictor will return a None if a dictionary does not contain your search path,
```
print(dictor(data, 'characters.Princess Leia'))

None
```
you can provide a default fallback value either by passing 
default="fallback value" or just placing a fallback string,
```
print(dictor(data, 'characters.Princess Leia', default='Not in Spaceballs'))

Not in spaceballs
```
or just add a fallback string,
```
print(dictor(data, 'characters.Princess Leia', 'fallback to this'))

fallback to this
```

if you want to error out on a None value, simply provide a CheckNone flag, a ValueError will be raised.
```
print(dictor(data, 'characters.Princess Leia', checknone=True))

Traceback (most recent call last):
  File "test.py", line 14, in <module>
    print(dictor(data, 'characters.Princess Leia', checknone=True))
  File "/github.com/dictor/dictor/__init__.py", line 77, in dictor
    raise ValueError('missing value for %s' % path)
ValueError: value not found for search path: "characters.Princess Leia"
```

---
## Passing a variable into search path
if you need to pass a variable into search path
```
who = "Barfolomew"
print(dictor(data, "characters.{}.id".format(who)))

55924
```
if using Python 3, you can also use F-strings

```
who = "Barfolomew"
print(dictor(data, f"characters.{who}.id"))
```
---

## List of Dicts
if the entire JSON structure is a list
```
[
 {
  "color": "red",
  "value": "#f00"
 },
 {
  "color": "green",
  "value": "#0f0"
 },
 {
  "color": "blue",
  "value": "#00f"
 }
]
```
just provide the list index into search path
```
print(dictor(data, ‘2.color’))

blue
```
---
## Nested List of lists
to parse a complex nested list of lists and dicts, just provide the list index in the search path

```
[
    {
        "type": "json",
        "message": [
            [
                {
                    "english": "apple",
                    "spanish": "manzana"
                },
                {
                    "english": "banana",
                    "spanish": "platano"
                }
            ],
            [
                {
                    "english": "cherry",
                    "spanish": "cereza"
                },
                {
                    "english": "durian",
                    "spanish": "durian",
                    "color": [
                        "black",
                        "brown",
                        "orange"
                    ]
                }
            ]
        ]
    }
]
```
dictor will parse each lookup element hierarchicly, starting with top and will work down to the last element, reading in each dot-separated list index.

```
print(dictor(data, '0.message.1.1.color.2'))

orange
```

---
## Handling Key lookups with dots

if you need to look up  a key value that has a dot in the key name, for example

```
{
    "dirty.harry": {
        "year": 1977,
        "genre": "romance"
    },
}
```

searching for dictor(data, 'dirty.harry') will return a None since Dictor sees the dot-separated entry as 2 separate keys.

To search for a key with a dot in it, simply use an escape character "\\.",
```
dictor(data, 'dirty\.harry')

{u'genre': u'romance', u'year': 1977}
```

---
## Testing
testing is done using Python Nose. Tests are located in 'tests' directory.
```
pip install nose

shell> nosetests test.py
```
---
## Release Notes

### 0.1.1
- removed "eval()" function for added security
- entire lookup engine was rewritten for increased speed and simplicy
- added 'ignorecase' parameter
- added ability to escape dot character for keys with dots in them
- looking up lists indexes was modified, 

    in previous version, looking up an element looked like this,
    ```
    dictor(data, 'characters.Dark Helmet.items[0]')
    ```
    new syntax is to place everything as a dot-separated path, this creates a single lookup standard, ie,
    ```
    dictor(data, 'characters.Dark Helmet.items.0')
    ```

### 0.0.1
- initial project released

---
## Contributors
- Mike Reider (May the Shwartz be with you)
