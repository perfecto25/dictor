# Dictor - the dictionary doctor
## An elegant dictionary and JSON handler

dictor takes a dictionary or JSON data and returns value for a specific key.

If dictor doesnt find a value for a key, or the data is missing the key, the return value is either None or whatever fallback value you provide as default="My Default Fallback value".

dictor is polite with Exception errors commonly encountered when parsing large Dictionaries/JSONs

## Installation
```
pip install dictor
```

## Examples

Heres a YAML representation of the JSON used in this example

sample.yaml
```
characters:
    Lonestar:
        id: 55923
        role: renegade
        items:
            - space winnebago
            - leather jacket
    Barfolomew:
        id: 55924
        role: mawg
        items:
            - peanut butter jar
            - waggy tail
    Dark Helmet:
        id: 99999
        role: Good is dumb
        items:
            - Shwartz
            - helmet
    Skroob:
        id: 12345
        role: Spaceballs CEO
        items:
            - luggage
```

same example YAML in JSON form

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
---
get only the 1st Item of a character
```
print(dictor(data, 'characters.Dark Helmet.items[0]'))

Shwartz
```
---


## Fallback Value & Error handling
by default, dictor will return a None if a dictionary does not contain your search path,
```
print(dictor(data, 'characters.Princess Leia'))

None
```
you can provide a default fallback value
```
print(dictor(data, 'characters.Princess Leia', default='This character was not in spaceballs'))

This character was not in spaceballs
```
if you want to error out on a None value, simply provide a CheckNone flag, a ValueError will be raised.
```
print(dictor(data, 'characters.Princess Leia', checknone=True))

Traceback (most recent call last):
  File "test.py", line 14, in <module>
    print(dictor(data, 'characters.Princess Leia', checknone=True))
  File "/github.com/dictor/dictor/__init__.py", line 77, in dictor
    raise ValueError('missing value for %s' % path)
ValueError: missing value for ['characters']['Princess Leia']
```

---
## Passing a variable into search path
if you need to pass a variable into search path
```
who = "Barfolomew"
print(dictor(data, "characters.{}.id".format(who)))

55924
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
    },
    {
        "type": "json",
        "message": "None"
    }
]
```
```
print(dictor(data, '0.message[1].1.color[2]'))

orange
```
---
## Testing
testing is done using Python Nose
```
pip install nose

shell> nosetests test.py
```