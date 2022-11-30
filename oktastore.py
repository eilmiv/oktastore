from collections import defaultdict
import json


def is_var(x):
    return str(x).startswith("_")

        
def queries(s, p, o):
    yield s, p, o
    yield s, p, "_0"
    yield s, "_0", o
    yield s, "_0", "_1"
    yield "_0", p, o
    yield "_0", p, "_1"
    yield "_0", "_1", o
    yield "_0", "_1", "_2"
    if p == o:
        yield "_0", "_1", "_1"
        yield s, "_0", "_0"
    if s == o:
        yield "_0", "_1", "_0"
        yield "_0", p, "_0"
    if s == p:
        yield "_0", "_0", "_1"
        yield "_0", "_0", o
    if s == p and p == o:
        yield "_0", "_0", "_0"      
          
 
def normalize(*triple):
    idx = 0
    mapping = dict()
    for x in triple:
        if is_var(x) and x not in mapping:
            mapping[x] = f"_{idx}"
            idx += 1
    return tuple(mapping.get(x, x) for x in triple)


class TripleStore:
    def __init__(self):
        self.index = defaultdict(set)

    def insert(self, *triple):
        for q in queries(*triple):
            self.index[q].add(triple)

    def remove(self, *triple):
        for q in queries(*triple):
            self.index[q].discard(triple)

    def query(self, *triple):
        return self.index[normalize(*triple)]
        
    def map_query(self, *triple):
        for result_triple in self.query(*triple):
            yield {
                var: val
                for var, val in zip(triple, result_triple)
                if is_var(var)
            }
        
    def multi_query(self, triples):
        if len(triples) == 0:
           yield dict()
           return
           
        triple = min(triples, key=lambda t: len(self.query(*t)))
        for mapping in self.map_query(*triple):
            sub_triples = [
                [mapping.get(x, x) for x in t]
                for t in triples 
                if t != triple
            ]
            for sub_mapping in self.multi_query(sub_triples):
                yield {**mapping, **sub_mapping}
    	

    def dump(self):
        return json.dumps(list(self.query("_0", "_1", "_2")))

    def load(self, json_string):
        for triple in json.loads(json_string):
            self.insert(*triple)
