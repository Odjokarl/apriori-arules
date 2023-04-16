#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "27.01.23"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__update__ = "27.01.23 11:26"

"""
utility for the Apriori class
"""
import copy

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

attr_types = {'dbase': dict,
              'candidates_sz': int,
              'candidates': dict,
              'current': dict,
              'support_history': dict}
lattr = sorted(attr_types.keys())

signatures = {'__init__': ([dict],),
              'reset': ([],),
              'support': ([float], dict),
              'scan_dbase': ([float],),
              'Lk': ([], list),
              'cross_product': ([],),
              'main': ([float], list)
              }
required = signatures.keys()

# tid might be anything values are list of int
samples = {1: {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]},
           2: {'a': [3,5,7], 'b':[3,5], 'c':[7,3], 'd':[5,7], 'e': [7,5],
               'f': [7,3,5], 'g':[7,5,3]},
           }

expected = {
    1:{
        'candidates': {
            300: [(1, 2), (1, 3), (1, 5), (2, 3), (2, 5), (3, 5)],
            100: [(1, 3), (1, 4), (3, 4)],
            200: [(2, 3), (2, 5), (3, 5)],
            400: [(2, 5)]},
        'current': {
            (1, 2): {300},
            (1, 3): {100, 300},
            (1, 4): {100},
            (1, 5): {300},
            (2, 3): {200, 300},
            (2, 4): set(),
            (2, 5): {200, 300, 400},
            (3, 4): {100},
            (3, 5): {200, 300},
            (4, 5): set()}
    },
    2:{
        'candidates': {
            'g': [(3, 5), (3, 7), (5, 7)],
            'f': [(3, 5), (3, 7), (5, 7)],
            'a': [(3, 5), (3, 7), (5, 7)],
            'b': [(3, 5)],
            'c': [(3, 7)],
            'd': [(5, 7)],
            'e': [(5, 7)]},
        'current': {
            (3, 5): {'g', 'f', 'a', 'b'},
            (3, 7): {'g', 'f', 'c', 'a'},
            (5, 7): {'d', 'e', 'g', 'a', 'f'}
            }
        }
}

resultat_main = [ {1: [[(1,), (2,), (3,), (4,), (5,)],
                       [(1, 2), (1, 3), (1, 4), (1, 5),
                        (2, 3), (2, 4), (2, 5),
                        (3, 4), (3, 5), (4, 5)],
                       [(1, 2, 3), (1, 2, 4), (1, 2, 5),
                        (1, 3, 4), (1, 3, 5), (1, 4, 5),
                        (2, 3, 4), (2, 3, 5), (2, 4, 5),
                        (3, 4, 5)],
                       [(1, 2, 3, 4), (1, 2, 3, 5), (1, 2, 4, 5),
                        (1, 3, 4, 5), (2, 3, 4, 5)],
                       [(1, 2, 3, 4, 5)]],
                2: [[(3,), (5,), (7,)], [(3, 5), (3, 7), (5, 7)], [(3, 5, 7)]]
                },
               {1: [[(1,), (2,), (3,), (5,)],
                    [(1, 3), (2, 3), (2, 5), (3, 5)],
                    [(2, 3, 5)]],
                2: [[(3,), (5,), (7,)],
                    [(3, 5), (3, 7), (5, 7)]],
                },
               {1: [],
                2: [],
                } ]
               
def enum_base(b:dict) -> dict:
    o = {k: [(x,) for x in v]
         for k,v in b.items() }
    return o
                
resultat_att = [ {1:{
    'current': {(1,2,3,4,5): set()},
    'candidates_sz': 5,
    'candidates': {},},
             2:{
                 'current': {(3, 5, 7): {'g', 'f', 'a'}},
                 'candidates_sz': 3,
                 'candidates': {x: [(3, 5, 7)] for x in 'gaf'},
             }}, # 0
            {1:{'current': {(2, 3, 5): {200, 300}},
                'candidates_sz': 3,
                'candidates': {200: [(2, 3, 5)], 300: [(2, 3, 5)]}},
             2:{'current': {},
                 'candidates_sz': 3,
                'candidates': {x: [(3, 5, 7)] for x in 'gaf'},
                },
             }, # .5
            {1:{'current': {},
                'candidates_sz': 1,
                'candidates': enum_base(samples[1])
                },
             2:{'current': {},
                'candidates_sz': 1,
                'candidates': enum_base(samples[2])
                },
             } # 1.
                ]
                 
def save(obj:any, latt:str) -> dict:
    return {att: copy.deepcopy(getattr(obj, att))
            for att in latt.split()}

