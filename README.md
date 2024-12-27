# oktastore
A very simple in-memory triplestore in pure python. Allows constant time queries.

## Installation
The store is so simple you can just copy the [oktastore.py](oktastore.py) file to your project.

Alternatively you can use pip:
```bash
pip install git+https://github.com/eilmiv/oktastore
```

## Usage
```python
from oktastore import TripleStore
store = TripleStore()

## Insert and remove triples:
store.insert(1, "is_half_of", 2)  # any hashable value can be part of the triple
store.insert(2, "is_half_of", 4)
store.insert(4, "is_half_of", 8)
store.remove(4, "is_half_of", 8)


## Queries:
store.query("_half", "is_half_of", "_total")  # variables start with "_"
# result: {(1, 'is_half_of', 2), (2, 'is_half_of', 4)}

len(store.query("_half", "is_half_of", "_total"))  # runs always in constant time!
# result: 2

list(store.multi_query([
    ("_quarter", "is_half_of", "_half"), ("_half", "is_half_of", "_total")
]))
# result: [{'_quarter': 1, '_half': 2, '_total': 4}]


## Store to / load from file:
with open("triples.csv", "w") as f:
    f.write(store.dump())  # uses repr() to dump the values

with open("triples.csv") as f:
    store.load(f.read())  # uses ast.literal_eval() to load the values
```

Example - serialization as json:
```python
import json
from oktastore import TripleStore
store = TripleStore()
store.insert(1, 2, 3)

# store as json
with open("graph.json", "w") as f:
    json.dump({"graph": list(store.query("_s", "_p", "_o"))}, f)

# load from json
with open("graph.json") as f:
    for triple in json.load(f)["graph"]:
        store.insert(*triple)
```


