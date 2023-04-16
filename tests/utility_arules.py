#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "30.01.23"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__update__ = "30.01.23 13:50"

"""
utility for the Arules class
"""
import copy
import pandas as pd

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

attr_types = {'list_itemsets': list,
              'support_itemsets': dict,
              'rules': list,
              }
lattr = sorted(attr_types.keys())

# each method with (list of types, type)
signatures = {'__init__': ([list, dict],),
              'reset': ([],),
              'support': ([tuple, tuple], float),
              'confidence': ([tuple, tuple], float),
              'lift': ([tuple, tuple], float),
              'leverage': ([tuple, tuple], float),
              'conviction': ([tuple, tuple], float),
              'lift_diag': ([tuple, tuple], str),
              'cross_product': ([list, int], list),
              'validation_rules': ([tuple, list, float], list),
              'build_rules': ([tuple, list, float],),
              'generate_rules': ([float],),
              'main': ([float], pd.DataFrame),
              }
required = signatures.keys()

samples = {1: ([[(1,), (2,), (3,), (4,)], [ (1,2), (1,4), (2,3)]], 
		{(1,): .5, (2,): .5, (3,): .5, (4,): .5, 
		 (1,2): .3, (1,4): .25, (2,3): .4}),
           2: ([[(1,), (2,), (3,), (5,)],
                [(1, 3), (2, 3), (2, 5), (3, 5)], [(2, 3, 5)]],
               {(1,): 0.5, (3,): 0.75, (2,): 0.75, (5,): 0.75,
                (1, 3): 0.5, (2, 3): 0.5, (2, 5): 0.75, (3, 5): 0.5,
                (2, 3, 5): 0.5}),
           3: ([[(3,), (5,), (7,)], [(5, 7)]],
               {(3,): 0.71, (5,): 0.86, (7,): 0.86, (5, 7): 0.71}),
           4: ([[(1,), (2,), (3,), (4,), (5,), (6,), (7,)],
                [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4),
                 (3, 4), (3, 5), (4, 5), (6, 7)],
                [(1, 2, 3), (1, 2, 4), (3, 4, 5)]],
               {(1,): 0.43, (2,): 0.57, (3,): 0.43, (4,): 0.57,
                (5,): 0.43, (6,): 0.29, (7,): 0.29, (1, 2): 0.43,
                (1, 3): 0.29, (1, 4): 0.29, (2, 3): 0.29, (2, 4): 0.29,
                (3, 4): 0.29, (3, 5): 0.29, (4, 5): 0.43, (6, 7): 0.29,
                (1, 2, 3): 0.29, (1, 2, 4): 0.29, (3, 4, 5): 0.29}),
           5: ([[(1,), (2,), (3,), (4,), (5,)], [(1, 2), (4, 5)]],
               {(1,): 0.43, (2,): 0.57, (3,): 0.43, (4,): 0.57, (5,): 0.43,
                (1, 2): 0.43, (4, 5): 0.43}),
           }
# sample_4.csv (4 1/4 ; 5 1/3)
meanings = ['', 'lait', 'pain', 'fruits', 'beurre',
            'oeufs', 'bieres', 'couches']

# (minSupp, maxitsets, minConf, a->b & b->a)
# if minConf < last output is identical
out_rules = {1: (.25, 2, {1.: (0,True),
                          .75: (2, True),
                          .5: (6, True),}),
             2: (.5, 3, {1.: (3, False),
                         .75: (3, False),
                         .5: (11, True),}),
             3: (.71, 2, {1.: (0, True),
                          .75: (2, True),}),
             4: (.29, 3, {1.: (4, False),
                          .75: (6, True),
                          .5: (27, True),}),
             5: (.43, 2, {1.: (2, False),
                          .75: (4,True),}),}
                          
                         
