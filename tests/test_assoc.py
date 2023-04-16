#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "30.01.23"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__update__ = "02.02.23 06:03"
__usage__="""
tests for the Arules class
"""

import os
import inspect
import unittest
from unittest.mock import patch
from tools import checkTools as chk
# 2 imports pour la méthode 'main'
import pandas as pd
import numpy as np

try:
    from utility_arules import *
except:
    print("failed to access ./utility_arules")
    try:
        from tests.utility_arules import *
    except:
        print("no access to test_utility")

CLASS='Arules'

class TestDefault(unittest.TestCase):
    """ verify the default behavior for Arules """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)
    @patch('builtins.print')
    def test_default(self, mock_prn:callable):
        """ all the required methods/attributes exist for Arules """
        self.o = self.K(*samples[1])
        for att in lattr:
            with self.subTest(att=att):
                self.assertTrue(hasattr(self.o, att),
                                "missing {}".format(att))
        for meth in required:
            with self.subTest(att=att):
                self.assertTrue(hasattr(self.o, meth),
                                "missing {}".format(meth))

    @patch('builtins.print')
    def test_surprising(self, mock_prn:callable):
        """ parse the internal dictionary for forbidden values in Arules """
        _keys = self.K.__dict__.keys()
        _authorized = lattr[:]
        _authorized.extend(required)

        for key in _keys:
            if key.startswith('__'): continue
            if key.startswith('_Arules__'): continue
            else:
                with self.subTest(att=key):
                    self.assertTrue(key in _authorized,
                                    "non authorized : {}".format(key))

    @patch('builtins.print')
    def test_signatures(self, mock_prn:callable):
        """ check signatures are set correctly for required meths of Arules """
        self.o = self.K(*samples[1])
        for meth in required:
            with self.subTest(meth=meth):
                _s = inspect.signature(getattr(self.o, meth))
                _e = signatures[meth]
                self.assertEqual(len(_s.parameters), len(_e[0]),
                                 "wrong number of parameters for {}"
                                 "".format(meth))
                for k,v in zip(_s.parameters, _e[0]):
                    _a = _s.parameters[k].annotation
                    self.assertEqual(_a, v,
                                     "expect type {} found type {}"
                                     "".format(_a,v))
                if len(_e) == 2:
                    self.assertEqual(_s.return_annotation, _e[1],
                                     "expect type {1} found type {0}"
                                     "".format(_s.return_annotation,_e[1]))
                else:
                    self.assertEqual(_s.return_annotation, inspect._empty,
                                     "expect 'empty' found type {}"
                                     "".format(_s.return_annotation))

class TestInit(unittest.TestCase):
    """ verify the init step """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_init(self, mock_prn:callable):
        """ Arules initialisation is fine """
        obj = self.K(*samples[1])
        chk.check_attr(obj, 'list_itemsets')
        _rep = obj.list_itemsets
        self.assertEqual(_rep, samples[1][0],
                         "found {} expect {}".format(_rep, samples[1][0]))
        chk.check_attr(obj, 'support_itemsets')
        _rep = obj.support_itemsets
        self.assertEqual(_rep, samples[1][1],
                         "found {} expect {}".format(_rep, samples[1][1]))

    @patch('builtins.print')
    def test_types(self, mock_prn:callable):
        """ do variables exist and are well typed in Arules """
        obj = self.K(*samples[1])
        chk.check_attr(obj, 'reset')
        for att in lattr: chk.check_attr(obj, att)
        for att in lattr:
            self.assertTrue(isinstance(getattr(obj, att),
                                       attr_types[att]),
                            "expect {} for '{}'".format(attr_types[att], att))

class TestReset(TestInit):
    """ verify the reset step """

    @patch('builtins.print')
    def test_reset(self, mock_prn:callable):
        """ typing test after reset of Arules """
        return self.test_types()

    def subtest(self, lst:list, dsupp:dict):
        """ Arules: given a sample, test reset/lattr """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'reset')
        for att in lattr: chk.check_attr(obj, att)
        _values = {att: getattr(obj, att) for att in lattr} # collect values
        # check content
        self.assertEqual(_values['list_itemsets'], lst,
                         "wrong itemsets")
        self.assertEqual(_values['support_itemsets'], dsupp,
                         "wrong itemsets support dictionnary")
        self.assertEqual(_values['rules'], [],
                         "wrong list of rules")
        _bag = set([])
        for x in [set(l) for l in lst]: _bag.update(x)
        _keys = set(dsupp.keys())
        self.assertEqual(_bag, _keys, "data are incoherent")

    @patch('builtins.print')
    def test_values(self, mock_prn:callable):
        """ Arules: test values after reset """
        for data in samples:
            with self.subTest(data=data):
                self.subtest(*samples[data])

class TestMetrics(unittest.TestCase):
    """ Arules: all about metrics """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    def subtest_support(self, lst:list, dsupp:dict):
        """ Arules: support (lhs U rhs) """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'support')
        _duo = lst[1]
        for x,y in _duo:
            _1, _2 = tuple([x]), tuple([y])
            _r1 = obj.support(_1,_2)
            _r2 = obj.support(_2,_1)
            self.assertTrue(abs(_r1 -dsupp[(x,y)])<1e-3, "a -> b")
            self.assertTrue(abs(_r2 -dsupp[(x,y)])<1e-3, "b -> a")
            self.assertTrue(_r1 == _r2, "should be same result")

    @patch('builtins.print')
    def test_support(self, mock_prn:callable):
        """ Arules: test support for some rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_support(*samples[data])

    def subtest_confidence(self, lst:list, dsupp:dict):
        """ Arules: support (lhs U rhs) / lhs """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'confidence')
        for p in (0,-1):
            for e in lst[-1]:
                r = list(e)
                a = r.pop(p)
                _1,_2 = tuple(r), tuple([a])
                _0 = obj.confidence(_1, _2)
                _0a = dsupp[e]/dsupp[_1]
                _1 = obj.confidence(_2, _1)
                _1a = dsupp[e]/dsupp[_2]
                self.assertTrue(abs(_0 - _0a)<1e-3, "{} -> {}".format(r,a))
                self.assertTrue(abs(_1 - _1a)<1e-3, "{} -> {}".format(a,r))


    @patch('builtins.print')
    def test_confidence(self, mock_prn:callable):
        """ Arules: test confidence for some rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_confidence(*samples[data])

    def subtest_lift(self, lst:list, dsupp:dict):
        """ Arules: support (lhs U rhs) / (lhs * rhs) """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'lift')
        for p in (0,-1):
            for e in lst[-1]:
                r = list(e)
                a = r.pop(p)
                _1,_2 = tuple(r), tuple([a])
                _0 = obj.lift(_1, _2)
                _0a = obj.lift(_2, _1)
                _0b = dsupp[e]/(dsupp[_1] * dsupp[_2])
                self.assertTrue(abs(_0 - _0b)<1e-3, "{} -> {}".format(r,a))
                self.assertTrue(abs(_0a - _0b)<1e-3, "{} -> {}".format(a,r))
                self.assertEqual(_0, _0a, "{} -> {}".format(r,a))


    @patch('builtins.print')
    def test_lift(self, mock_prn:callable):
        """ Arules: test lift for some rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_lift(*samples[data])

    def subtest_leverage(self, lst:list, dsupp:dict):
        """ Arules: support (lhs U rhs) - (lhs * rhs) """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'leverage')
        for p in (0,-1):
            for e in lst[-1]:
                r = list(e)
                a = r.pop(p)
                _1,_2 = tuple(r), tuple([a])
                _0 = obj.leverage(_1, _2)
                _0a = obj.leverage(_2, _1)
                _0b = dsupp[e] - (dsupp[_1] * dsupp[_2])
                self.assertTrue(abs(_0 - _0b)<1e-3, "{} -> {}".format(r,a))
                self.assertTrue(abs(_0a - _0b)<1e-3, "{} -> {}".format(a,r))
                self.assertEqual(_0, _0a, "{} -> {}".format(r,a))


    @patch('builtins.print')
    def test_leverage(self, mock_prn:callable):
        """ Arules: test leverage for some rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_leverage(*samples[data])
                

    def subtest_conviction(self,  lst:list, dsupp:dict):
        """ Arules: (1 - rhs) / (1 - confidence) """
        obj = self.K(lst, dsupp)
        chk.check_attr(obj, 'conviction')
        for p in (0,-1):
            for e in lst[-1]:
                r = list(e)
                a = r.pop(p)
                _1,_2 = tuple(r), tuple([a])
                _conf = dsupp[e]/dsupp[_1]
                _0 = obj.conviction(_1, _2)
                if _conf==1:
                    self.assertIsNone(_0, "expect None got {}".format(_0))
                else:
                    _a = (1-dsupp[_2])/(1-_conf)
                    self.assertTrue(abs(_0 -_a)<1e-3, "{}".format(_0-_a))
                _conf = dsupp[e]/dsupp[_2]
                _0 = obj.conviction(_2, _1)
                if _conf==1:
                    self.assertIsNone(_0, "expect None got {}".format(_0))
                else:
                    _a = (1-dsupp[_1])/(1-_conf)
                    self.assertTrue(abs(_0 -_a)<1e-3, "2:{}".format(_0-_a))

    @patch('builtins.print')
    def test_conviction(self, mock_prn:callable):
        """ Arules: test conviction for some rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_conviction(*samples[data])

    @patch('builtins.print')
    def test_lift_diag(self, mock_prn:callable):
        """ Arules: test lift diagnostic content """
        obj = self.K(*samples[2])
        chk.check_attr(obj, 'lift_diag')
        lhs, rhs = (2,5), (3,) # lift < 1
        _0 = obj.lift_diag(lhs, rhs)
        self.assertTrue(str(lhs) in _0)
        self.assertTrue(str(rhs) in _0)
        _msg = "ne peuvent pas co-exister dans une règle"
        self.assertTrue(_msg in _0,
                        "missing '{}' got <{}>".format(_msg, _0))
        lhs, rhs = (2,3), (5,) # lift > 1
        _0 = obj.lift_diag(lhs, rhs)
        self.assertTrue(str(lhs) in _0)
        self.assertTrue(str(rhs) in _0)
        _msg = "est prédictive"
        self.assertTrue(_msg in _0,
                        "missing '{}' got <{}>".format(_msg, _0))
        obj = self.K([ [(1,), (2,)], [(1,2)] ],
                     {(1,): 1, (2,): 1, (1,2): 1})
        lhs, rhs = (2,), (1,) # lift = 1
        _0 = obj.lift_diag(lhs, rhs)
        self.assertTrue(str(lhs) in _0)
        self.assertTrue(str(rhs) in _0)
        _msg = "ne pas utiliser"
        self.assertTrue(_msg in _0,
                        "missing '{}' got <{}>".format(_msg, _0))

class TestAlgorithm(unittest.TestCase):
    """ Arules: all about rules generation """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_basic_crossproduct(self, mock_prn:callable):
        """ Arules: test simple cross_product """
        obj = self.K(*samples[1])
        chk.check_attr(obj, 'cross_product')
        _s = [ (1,2), (1,3), (2,3) ]
        _o = obj.cross_product(_s, 2)
        self.assertTrue(isinstance(_o, list), "wrong output type")
        self.assertTrue(len(_o) == 1, "wrong content")
        self.assertTrue(isinstance(_o[0], tuple), "wrong type of itemset")
        self.assertTrue(len(_o[0])==3, "wrong len of itemset")
        self.assertTrue(tuple(sorted(_o[0]))==_o[0], "badly sorted")

    def subtest_crossproduct(self, lst:list, supp:dict):
        obj = self.K(lst, supp)
        chk.check_attr(obj, 'cross_product')
        for p in range(len(lst)-1):
            _o = obj.cross_product(lst[p], p+1)
            self.assertTrue(set(_o).issuperset(lst[p+1]),
                            "expect {} subpart of {}"
                            "".format(lst[p+1], _o))
            self.assertTrue(_o == sorted(_o),
                            "expect sorted, found {}".format(_o))
            if len(_o) > 1:
                self.assertTrue(all([len(x)==p+2
                                     for x in _o]),
                                "bad size of itemsets\n {} -> {}"
                                "".format(p+1, _o))
                
    @patch('builtins.print')
    def test_smart_crossproduct(self, mock_prn:callable):
        """ Arules: test smart cross_product """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_crossproduct(*samples[data])

    @patch('builtins.print')
    def test_simple_validation(self, mock_prn:callable):
        """ Arules: test simple validation_rules """
        obj = self.K(*samples[2])
        chk.check_attr(obj, 'validation_rules')
        chk.check_attr(obj, 'rules')
        chk.check_attr(obj, 'confidence')
        _c = [(2,), (3,), (5,), (2,3), (2,5), (3,5)]
        _s = 3/4
        _g = (2,3,5)
        _o = obj.validation_rules( _g, _c, _s)
        _r = obj.rules.copy()
        for a,b in _r:
            self.assertTrue(obj.confidence(a,b) >= _s,
                            "rules {} -> {} is bad".format(a,b))
            self.assertTrue(b in _c, "{} is not in candidates"
                            "".format(b))
            self.assertTrue(set(a+b) == set(_g),
                            "wrong rule {}+{} != {}".format(a,b,_g))
        self.assertEqual(_o, [(2,), (5,)],
                         "wrong output of validation")

    
    @patch('builtins.print')
    def test_simple_build(self, mock_prn:callable):
        """ Arules: test simple build_rules """
        obj = self.K(*samples[2])
        chk.check_attr(obj, 'build_rules')
        chk.check_attr(obj, 'rules')
        _itset = (2,3,5)
        _rhs = [ tuple([x]) for x in _itset ]
        for v in range(1,7):
            with self.subTest(seuil="1/{}".format(v)):
                _old = len(obj.rules)
                _o = obj.build_rules(_itset, _rhs, 1/v)
                _new = len(obj.rules)
                self.assertIsNone(_o, "'build_rules' should"
                                  " not return anything")
                if v == 1:
                    self.assertTrue(_old == 0, "rules are empty")
                    self.assertTrue(_new == 0, "rules are empty")
                else:
                    self.assertTrue(_old+3 == _new, "rules grow by 3")
                    if v > 2:
                        self.assertTrue(_old>0, "rules should not be empty")

    def subtest_genrules(self, key:int):
        obj = self.K(*samples[key])
        chk.check_attr(obj, 'generate_rules')
        chk.check_attr(obj, 'rules')
        _minSupp, sz_itset, dic = out_rules[key]
        _old = 0
        for k in dic:
            with self.subTest(minConf=k):
                _current = len(obj.rules)
                self.assertEqual(_old, _current, "rules have been changed")
                _out = obj.generate_rules(k)
                self.assertIsNone(_out,
                                  "expect no return from 'generate_rules'")
                _old = len(obj.rules)
                self.assertEqual(dic[k][0], _old,
                                 "expect {} rules found {}"
                                 "".format(dic[k][0], _old))
    @patch('builtins.print')
    def test_simple_generate(self, mock_prn:callable):
        """ Arules: test simple generate_rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_genrules(data)


class TestMain(unittest.TestCase):
    """ Arules: all about pd.DataFrame output """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)
        chk.check_attr(self.K, 'main')
        self.meth = "support confidence lift leverage conviction".split()
        self.cols = ['lhs', 'rhs', 'lhs_support', 'rhs_support']
        
    @patch('builtins.print')
    def test_columns(self, mock_prn:callable):
        """ Arules: main provides the good columns """
        obj = self.K(*samples[1])
        _df = obj.main(1)
        for m in self.meth: chk.check_attr(obj, m)
        for k in self.cols+self.meth:
            self.assertTrue(k in _df.columns,
                            "{} not found in {}".format(k, _df.columns))

    def subtest_genrules(self, key:int):
        obj = self.K(*samples[key])
        chk.check_attr(obj, 'rules')
        _minSupp, sz_itset, dic = out_rules[key]
        _nine = len(self.cols+self.meth)
        _old = 0
        for k in dic:
            with self.subTest(minConf=k):
                _current = len(obj.rules)
                self.assertEqual(_old, _current, "rules have been changed")
                _out = obj.main(k)
                self.assertTrue(_out.shape==(dic[k][0],_nine),
                                  "expect {}".format( (dic[k][0],_nine) ))
                _old = len(obj.rules)
                self.assertEqual(dic[k][0], _old,
                                 "expect {} rules found {}"
                                 "".format(dic[k][0], _old))
    @patch('builtins.print')
    def test_size(self, mock_prn:callable):
        """ Arules: main provides the right rules """
        for data in samples:
            with self.subTest(data=data):
                self.subtest_genrules(data)
    
#================= link to main_tests =======================#
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestDefault, TestInit, TestReset, TestMetrics,
               TestAlgorithm, TestMain)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet
        
