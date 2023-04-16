#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__author__ = "Ulrich Karl ODJO && Augusta Mwinja Kachungunu"
__date__ = "10.03.23"
__usage__ = "arules class"

from apriori import Apriori
import numpy as np
from pandas import DataFrame

class Arules(object):
    def __init__(self, list_itemsets: list, support_itemsets: dict):
        self.list_itemsets = list_itemsets
        self.support_itemsets = support_itemsets
        self.reset()

    def reset(self):
        self.rules = []

    def support(self, litemset: tuple, ritemset:tuple) -> float:
        item = tuple(sorted(list(litemset+ritemset)))
        return self.support_itemsets[item]

    def confidence(self, litemset: tuple, ritemset: tuple) -> float:
        return self.support(litemset, ritemset) / self.support_itemsets[litemset]

    def lift(self, litemset: tuple, ritemset: tuple) -> float:
        return self.confidence(litemset, ritemset) * (1 / self.support_itemsets[ritemset])

    def leverage(self, litemset: tuple, ritemset: tuple) -> float:
        return self.support(litemset, ritemset) - (self.support_itemsets[litemset] * self.support_itemsets[ritemset])

    def conviction(self, litemset: tuple, ritemset: tuple) -> float:
        try:
            (1 - self.support_itemsets[ritemset]) / (1 - self.confidence(litemset, ritemset))
        except ZeroDivisionError:
            return None
        else:
            return (1 - self.support_itemsets[ritemset]) / (1 - self.confidence(litemset, ritemset))

    def lift_diag(self, lhs: tuple, rhs: tuple) -> str:
        if self.lift(lhs, rhs) == 1:
            return f"ne pas utiliser {lhs} -> {rhs}"
        elif self.lift(lhs, rhs) < 1:
            return f"{lhs} et {rhs} ne peuvent pas co-exister dans une règle"
        else:
            return f"{lhs} -> {rhs} est prédictive"

    def cross_product(self, L: list, k: int) -> list:
        rep = []
        taille = len(L)
        for i in range(taille-1):
            j = i + 1
            while j < taille and L[i][:-1] == L[j][:-1]:
                new = L[i] + L[j][-1:]
                ok = True
                idx = 0
                while idx < k+1 and ok:
                    ok = new[:idx] + new[idx+1:] in L
                    idx += 1
                if ok:
                    rep.append(new)
                j += 1
        return rep

    def validation_rules(self, lk: tuple, RHS: list, threshold: float) -> list:
        rhs_rules_accepted = []
        for item in RHS:
            leftitemset = tuple(sorted(set(lk) - set(item)))
            score_rules = self.confidence(leftitemset, item)
            if score_rules >= threshold:
                rhs_rules_accepted.append(item)
                self.rules.append((leftitemset, item))
        return rhs_rules_accepted

    def build_rules(self, lk: tuple, RHS: list, threshold: float):
        k = len(lk)
        sz_rhs = 1
        liste_rhs = RHS
        while len(liste_rhs) > 1 and k > sz_rhs + 1:
            liste_rhs = self.cross_product(liste_rhs, sz_rhs)
            liste_rhs = self.validation_rules(lk, liste_rhs, threshold)
            sz_rhs += 1

    def generate_rules(self, threshold: float):
        self.reset()
        for lk_items in self.list_itemsets:
            if len(lk_items[0]) == 1:
                continue
            elif len(lk_items[0]) == 2:
                for items in lk_items:
                    rhs = [(i,) for i in items]
                    self.validation_rules(items, rhs, threshold)
            else:
                for items in lk_items:
                    rhs = [(i,) for i in items]
                    self.build_rules(items, rhs, threshold)

    def main(self, minthreshold: float) -> DataFrame:
        self.generate_rules(minthreshold)
        data = {'lhs': [items[0] for items in self.rules],
                'rhs': [items[1] for items in self.rules],
                'lhs_support': [self.support_itemsets[items[0]] for items in self.rules],
                'rhs_support': [self.support_itemsets[items[1]] for items in self.rules],
                'support': [self.support(items[0], items[1]) for items in self.rules],
                'confidence': [self.confidence(items[0], items[1]) for items in self.rules],
                'lift': [self.lift(items[0], items[1]) for items in self.rules],
                'leverage': [self.leverage(items[0], items[1]) for items in self.rules],
                'conviction': [self.conviction(items[0], items[1]) if self.conviction(items[0], items[1]) != None else np.inf for items in self.rules]
                }
        return DataFrame(data)

if __name__ == "__main__":
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
    data = {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]}
    db = Apriori(data)
    br = Arules(db.main(.5), db.support_history)
    for k in range(1, 7):
        _ = br.main(1/k)
        print("min confidence 1/{}={:.3f}".format(k,1/k))
        print(_.head())
        print('*'*7)
