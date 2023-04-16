#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apriori import Apriori
from arules import Arules

ar = Arules([[(1,), (2,), (3,), (4,)], [ (1,2), (1,4), (2,3)]],
                {(1,): .5, (2,): .5, (3,): .5, (4,): .5,
                 (1,2): .3, (1,4): .25, (2,3): .4})
print("items", ar.list_itemsets)
print("support", ar.support_itemsets)
print("regles", ar.rules)
print("{0} Exemple 2 {0}".format("="*7))
data = {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]}
db = Apriori(data)
br = Arules(db.main(.5), db.support_history)
print("items", br.list_itemsets)
print("support", br.support_itemsets)
print("regles", br.rules)
print("#=== Evaluation des règles à partir du triplet (2,3,5) ===#")
for lhs,rhs in [ [(2,5), (3,)], [(2,3), (5,)], [(3,5), (2,)] ]:
    print("evaluation de {} -> {}".format(lhs, rhs))
    for m in "support confidence conviction leverage lift lift_diag".split():
        _r = getattr(br, m)(lhs, rhs)
        _r = round(_r, 3) if isinstance(_r, float) else _r
    print("{} : {}".format(getattr(br, m).__name__, _r))
    print("#"+"="*73+"#")
print("#=== Evaluation de cross product ====#")
print("{}".format(br.cross_product([(1,2), (1,3), (2,3), (2,4)], 2)))
print("#=== Evaluation de validation_rules ===")
print("rules before validation", br.rules)
_candidates = [(2,), (3,), (5,), (2,3), (2,5), (3,5)]
threshold = 3/4
print("candidates {} and minConfidence is {:.2f}".format(_candidates, threshold))
_out = br.validation_rules((2,3,5), _candidates, threshold)
print("rules after validation", br.rules)
print("accepted rhs", _out)
print(f"#{'='*73}#")
print("{0} generate_rules {0}".format('*=*'))
data = {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]}
db = Apriori(data)
br = Arules(db.main(.5), db.support_history)
for k in (.75, .5, .25, .1):
    print("min confiance", k)
    print("rules before generation", br.rules)
    _out = br.generate_rules( k )
    print("rules after generate_rules", br.rules)
    print("return of generate_rules ?", _out)
    print("*"*17)
print(f"#{'='*73}#")
print("{0} main {0}".format('*=*'))
data = {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]}
db = Apriori(data)
br = Arules(db.main(.5), db.support_history)
for k in range(1, 7):
    _ = br.main(1/k)
    print("min confidence 1/{}={:.3f}".format(k,1/k))
    print(_.head())
    print('*'*7)
