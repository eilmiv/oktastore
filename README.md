# oktastore
A very simple in-memory triplestore in pure python. Allows constant time queries.

Usage:
```python
>>> from oktastore import TripleStore
>>> store = TripleStore()

>>> store.insert(1, "is_half_of", 2)  # any hashable value can be part of the triple
>>> store.insert(2, "is_half_of", 4)

>>> store.query("_half", "is_half_of", "_total")  # variables start with "_"
{(1, 'is_half_of', 2), (2, 'is_half_of', 4)}
>>> len(store.query("_half", "is_half_of", "_total"))  # runs always in constant time!
2
>>> list(store.multi_query([
        ("_quarter", "is_half_of", "_half"), ("_half", "is_half_of", "_total")
    ]))
[{'_quarter': 1, '_half': 2, '_total': 4}]
```
