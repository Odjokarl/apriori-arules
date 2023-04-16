#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "27.01.23"
__usage__ = "Test loader pour Apriori/Arules"
__update__ = "27.01.23 11h54"

import os
import sys
import unittest
from tools.checkTools import *

#===== tests import, will grow ==========#
try:
    from tests import test_apriori
except Exception as _e:
    print(_e, "failed test_apriori")
    pass
try:
    from tests import test_assoc
except Exception as _e:
    print(_e, "failed test_assoc")
    pass
#========================================#

#================================ unittest area ========================#
def suite_me(fname, toTest):
    if not hasattr(toTest, '__iter__'): raise TypeError("go to Hell !")
    print("Vous avez {} série(s) à passer".format(len(toTest)))
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    suite = unittest.TestSuite()
    for test_me in toTest:
        try:
            suite.addTest(test_me.suite(fname))
        except Exception as _e:
            print(_e)
            
    return suite

if __name__ == '__main__':

    if len(sys.argv) == 1:
        param = input("quel est le fichier à traiter ? ")
        if not os.path.isfile(param): ValueError("need a python file")
    else: param = sys.argv[1]

    target = param.split('.')[0]

    _out = check_property(target != '','acces au fichier')
    print("tentative de lecture de {}".format(target))
    try:
        tp = __import__(target) # revient à faire import XXX as tp
    except Exception as _e:
        print(_e)
        sys.exit(-1)


    _test_names = {"apriori": [test_apriori],
                   "arules": [test_assoc],
                   "bahlsen": []}
    _yes = "oO0Yy"
    print("select wich subtests you want")
    print("Pour répondre par oui, utiliser l'un des symboles '{}'"
          "".format(_yes))
    _todo = []
    _ = input("passer tous les tests ? ")
    if len(_) >=1 and _[0] in _yes:
        for key in _test_names:
            _todo.extend(_test_names[key])
    else:
        for key in _test_names:
            if _test_names[key] == []: continue
            _ = input("passer les tests '{}' ? ".format(key))
            if len(_) >=1 and _[0] in _yes:
                _todo.extend(_test_names[key])
            
    unittest.TextTestRunner(verbosity=2).run(suite_me(target, _todo))
