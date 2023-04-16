#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "27.01.23"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__update__ = "06.01.23 15:50"
__usage__="""
tests for the Apriori class
"""

import os
import inspect
import unittest
from unittest.mock import patch
from tools import checkTools as chk
from copy import deepcopy as dcop

try:
    from utility_apriori import *
except:
    print("failed to access ./utility_apriori")
    try:
        from tests.utility_apriori import *
    except:
        print("no access to test_utility")

CLASS='Apriori'

class TestDefault(unittest.TestCase):
    """ Apriori: verify the default behavior """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_default(self, mock_prn:callable):
        """ Apriori: all the required methods/attributes exist """
        obj = self.K(samples[1])
        for att in lattr:
            with self.subTest(att=att):
                self.assertTrue(hasattr(obj, att),
                                "missing {}".format(att))
        for meth in required:
            with self.subTest(att=att):
                self.assertTrue(hasattr(obj, meth),
                                "missing {}".format(meth))

    @patch('builtins.print')
    def test_surprising(self, mock_prn:callable):
        """ Apriori: parse the internal dictionary for forbidden values """
        _keys = self.K.__dict__.keys()
        _authorized = lattr[:]
        _authorized.extend(required)

        for key in _keys:
            if key.startswith('__'): continue
            if key.startswith('_Apriori__'): continue
            else:
                with self.subTest(att=key):
                    self.assertTrue(key in _authorized,
                                    "non authorized : {}".format(key))

    @patch('builtins.print')
    def test_signatures(self, mock_prn:callable):
        """ Apriori: check signatures are set correctly for required meths """
        obj = self.K(samples[1])
        for meth in required:
            with self.subTest(meth=meth):
                chk.check_attr(obj, meth)
                _s = inspect.signature(getattr(obj, meth))
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
    """ Apriori: verify the init step """
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_init(self, mock_prn:callable):
        """ Apriori: initialisation is fine """
        obj = self.K(samples[1])
        chk.check_attr(obj, 'dbase')
        _rep = obj.dbase
        self.assertEqual(_rep, samples[1],
                         "found {} expect {}".format(_rep, samples[1]))

    @patch('builtins.print')
    def test_types(self, mock_prn:callable):
        """ Apriori: do variables exist and are well typed """
        obj = self.K(samples[1])
        chk.check_attr(obj, 'reset')
        for att in lattr: chk.check_attr(obj, att)
        for att in lattr:
            self.assertTrue(isinstance(getattr(obj, att),
                                       attr_types[att]),
                            "expect {} for '{}'".format(attr_types[att], att))
        
class TestReset(TestInit):
    """ Apriori: verify the reset step """

    @patch('builtins.print')
    def test_reset(self, mock_prn:callable):
        """ Apriori: typing test after reset """
        return self.test_types()

    def subtest(self, mykey:int):
        """ Apriori: for one sample test many """
        _local = {1: {'candidates': 4, 'current': 5},
                 2: {'candidates': 7, 'current': 3}, }
        
        sample = samples[mykey]
        obj = self.K(sample)
        chk.check_attr(obj, 'reset')
        obj.reset() # explicit call
        for att in lattr: chk.check_attr(obj, att)
        _values = {att: getattr(obj, att)
                   for att in lattr} # collect values
        self.assertEqual(_values['candidates_sz'], 1,
                         "wrong current itemsets, found {}"
                         "".format(_values['candidates_sz']))
    
        self.assertEqual(len(_values['support_history']), 0,
                         "wrong history, found {}"
                         "".format(len(_values['support_history'])))
        _d = _values['candidates']
        _what_expect = _local[mykey]['candidates']
        self.assertTrue(len(_d) == _what_expect,
                        "'candidates': found {}, expect {} values"
                        "".format(len(_d), _what_expect))
        for key in _d:
            # expect key in data
            self.assertTrue(key in sample, "unknow tid '{}'"
                            "".format(key))
            # expect list of tuples of length 1
            self.assertTrue(isinstance(_d[key], list),
                            "bad type for values in '{}' in 'self.candidates'"
                            "".format(key))
            for v in _d[key]:
                self.assertTrue(isinstance(v, tuple),
                                "bad type for {} in '{}'"
                                "".format(v,key))
                self.assertTrue(len(v) == 1,
                                "bad size for {} in '{}'"
                                "".format(v,key))
        _d = _values['current']
        _what_expect = _local[mykey]['current']
        self.assertTrue(len(_d) == _what_expect,
                        "'current': found {}, expect {} values"
                        "".format(len(_d), _what_expect))
                        
        for key in _d:
            self.assertTrue(isinstance(key, tuple),
                            "wrong type for '{}' in self.current"
                            "".format(key))
            self.assertTrue(len(key) == 1,
                            "wrong size for '{}' in self.current"
                            "".format(key))
            # expect set of tids
            self.assertTrue(isinstance(_d[key], set),
                            "bad type for value at '{}' in 'self.current'"
                            "".format(key))
            
            self.assertTrue(_d[key].issubset(sample.keys()),
                            "wrong tids for '{}' in 'self.current'"
                            "".format(key))
        
    @patch('builtins.print')
    def test_values(self, mock_prn:callable):
        """ Apriori: test values after reset """
        for data in samples:
            with self.subTest(data=data):
                self.subtest(data)

class TestSupport(unittest.TestCase):
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    def subtest(self, base:dict, minsupp:float) -> tuple:
        """ Apriori: one sample at a time """
        obj = self.K(base)
        chk.check_attr(obj, 'reset')
        chk.check_attr(obj, 'support')
        # 1 save the current
        _c = getattr(obj, 'current')
        # build the info needed
        _o = obj.support(minsupp)
        # _o keys() belongs to _c.keys()
        self.assertTrue(set(_o.keys()).issubset(_c.keys()),
                        "some keys are unknown: {}".format(_o.keys()))
        # values are in [minsupp, 1]
        for v in _o.values():
            self.assertTrue(isinstance(v, float),
                            "wrong type for {} expect a float".format(v))
            self.assertTrue(minsupp <= v <= 1,
                            "out of range {}".format(v))
        return (_o, _c)

    @patch('builtins.print')
    def test_lowsupp(self, mock_prn:callable):
        """ Apriori: for low support we expect huge results """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 0)
                # post-analyse
                self.assertEqual(sorted(_you[0].keys()),
                                 sorted(_you[1].keys()),
                                 "you missed some itemsets")

    @patch('builtins.print')
    def test_highsupp(self, mock_prn:callable):
        """ Apriori: for high support we expect few results """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 1)
                # post-analyse
                self.assertTrue(len(sorted(_you[0].keys())) < len(sorted(_you[1].keys())),
                                 "you picked too much itemsets")
                
    @patch('builtins.print')
    def test_mediumsupp(self, mock_prn:callable):
        """ Apriori: for mid support we expect some results """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], .5)
                # post-analyse
                _b = {k:len(v) for k,v in _you[1].items()}
                _n = len(samples[data])
                _e = [k for k,v in _b.items() if v>=_n/2]
                self.assertEqual(sorted(_you[0].keys()), sorted(_e),
                                 "expect {} found {}"
                                 "".format(_e, _you[0].keys()))
        
class TestScan(unittest.TestCase):
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    def subtest(self, base:dict, msupp:float, clean:bool) -> dict:
        """ Apriori: check that we change what is supposed to change """
        obj = self.K(base)
        chk.check_attr(obj, 'reset')
        chk.check_attr(obj, 'support')
        chk.check_attr(obj, 'scan_dbase')
        self.assertTrue(obj.support_history == {},
                        "support_history is not empty")

        if not clean:
            _bag = set()
            for k,v in base.items(): _bag.update(v)
            for i,x in enumerate(_bag):
                obj.support_history[tuple([x])] = 10+i
                if i>3: break
        _s = obj.support(msupp)
        _rep = {"old_{}".format(att): dcop(getattr(obj, att))
                for att in "candidates current support_history".split()}
        obj.scan_dbase(msupp)

        _rep['support'] = dcop(_s)
        for att in lattr:
            if att == 'dbase': continue
            _rep[att] = dcop(getattr(obj, att))

        self.assertEqual(_rep['support'].keys(), _rep['current'].keys(),
                         "keys should be equals in {} & {}"
                         "".format(_rep['support'].keys(),
                                   _rep['current'].keys()))
        return _rep
    
    @patch('builtins.print')
    def test_pure_scan_low(self, mock_prn:callable):
        """ Apriori: check that scan is fine for low support """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 0, True)
                self.assertEqual(_you['support_history'].keys(),
                                 _you['current'].keys(),
                                 "bad keys found in 'support_history' or"
                                 " and 'current'")
                self.assertEqual(_you['old_current'],
                                    _you['current'])
                                 
    @patch('builtins.print')
    def test_pure_scan_high(self, mock_prn:callable):
        """ Apriori: check that scan is fine for high support """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 1, True)
                self.assertEqual(_you['support_history'].keys(),
                                 _you['current'].keys(),
                                 "bad keys found in 'support_history' or"
                                 " and 'current'")
                self.assertEqual(_you['support_history'], {},
                                 "expect an empty history")
                self.assertEqual(_you['current'], {},
                                 "expect an empty 'current'")
                self.assertNotEqual(_you['old_current'],
                                    _you['current'])
                
    @patch('builtins.print')
    def test_pure_scan_mid(self, mock_prn:callable):
        """ Apriori: check that scan is fine for mid support """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], .5, True)
                self.assertEqual(_you['support_history'].keys(),
                                 _you['current'].keys(),
                                 "bad keys found in 'support_history' or"
                                 " and 'current'")
                                 

    @patch('builtins.print')
    def test_dirty_scan_low(self, mock_prn:callable):
        """ Apriori: check that scan is fine for low support & bogus values """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 0, False)
                self.assertEqual(_you['support_history'].keys(),
                                 _you['current'].keys(),
                                 "bad keys found in 'support_history' or"
                                 " and 'current'")
                self.assertEqual(_you['old_current'],
                                    _you['current'])
                
    @patch('builtins.print')
    def test_dirty_scan_high(self, mock_prn:callable):
        """ Apriori: check that scan is fine for high support & bogus values """
        for data in samples:
            with self.subTest(data=data):
                _you = self.subtest(samples[data], 1., False)
                self.assertFalse(_you['support_history'] == {},
                                 "expect a non empty history")
                self.assertEqual(_you['current'], {},
                                 "expect an empty 'current'")

    @patch('builtins.print')
    def test_dirty_scan_mid(self, mock_prn:callable):
        """ Apriori: check that scan is fine for mid support & bogus values """
        for data in (1,2):
            with self.subTest(data=data):
                _you = self.subtest(samples[data], .75, False)
                self.assertNotEqual(_you['support_history'].keys(),
                                 _you['current'].keys(),
                                 "bad keys found in 'support_history' or"
                                 " and 'current'")
                self.assertNotEqual(_you['support_history'],
                                    _you['old_support_history'].keys(),
                                    "some values should have changed")

class TestLk(unittest.TestCase):
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_lk(self, mock_prn:callable):
        """ Apriori: simple verification of k tuples """
        for data in samples:
            with self.subTest(data=data):
                base = samples[data]
                obj = self.K(base)
                chk.check_attr(obj, 'Lk')
                _out = obj.Lk()
                self.assertTrue(set(_out) == set(obj.current),
                                 "Lk should send the keys of 'current'")

                for i in range(len(_out)-1):
                    for j in range(i+1, len(_out)):
                        self.assertTrue(_out[i][0]<_out[j][0],
                                        "bad ranking")

class TestProduct(unittest.TestCase):
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    def subtest(self, base) -> dict:
        """ Apriori: load base, compute the 2-tuples """
        obj = self.K(base)
        chk.check_attr(obj, 'Lk')
        chk.check_attr(obj, 'cross_product')
        _vars = "candidates candidates_sz support_history current"
        for att in _vars.split(): chk.check_attr(obj, att)
        _old = save(obj, _vars)
        obj.cross_product()
        _new = save(obj, _vars)
        self.assertTrue(_old['candidates_sz']+1 == _new['candidates_sz'],
                        "wrong size of keys")
        self.assertTrue(_old['support_history']==_new['support_history'],
                        "'support_history' must be the same")

        return _new
    
    @patch('builtins.print')
    def test_product(self, mock_prn:callable):
        """ Apriori: load base and perform next step """
        for data in samples:
            with self.subTest(data=data):
                _out = self.subtest(samples[data])
                self.assertTrue(_out['support_history']=={},
                                "history should be empty")
                for k in "candidates current".split():
                    self.assertEqual(_out[k], expected[data][k],
                                     "wrong values for '{}'".format(k))
                
    @patch('builtins.print')
    def test_twisted_product(self, mock_prn:callable):
        """ Apriori: verify computation, with a twisted current """
        obj = self.K({})
        chk.check_attr(obj, 'Lk')
        chk.check_attr(obj, 'cross_product')
        _vars = "candidates candidates_sz support_history current"
        for att in _vars.split(): chk.check_attr(obj, att)
        # a stupid and fake current
        obj.current = {(1,2): {100}, (1,3): {100, 200},
                       (1,4): {100}, (2,3): {100, 200},
                       (2,4): {300}, (3,4,5): {12} }
        obj.candidates_sz = 2
        obj.candidates = {v: [k for k in obj.current
                              if v in obj.current[k]]
                          for v in (100, 200, 300, 12)}
        _old = save(obj, _vars)
        obj.cross_product()
        _new = save(obj, _vars)
        _expect = {'candidates': {100: [(1, 2, 3), (1, 2, 4)]},
                   'support_history': {},
                   'current': {(1, 2, 3): {100}, (1, 2, 4): {100}},
                   'candidates_sz':3}
        
        self.assertTrue(_old['candidates_sz']+1 == _new['candidates_sz'],
                        "wrong size of keys")
        self.assertTrue(_old['support_history']==_new['support_history'],
                        "'support_history' must be the same")
        for att in _expect:
            self.assertEqual(_new[att], _expect[att],
                         "wrong '{0}\nfound {1}\n expect {2}"
                         "".format(att, _new[att], _expect[att]))
        
        

class TestMain(unittest.TestCase):
    def setUp(self):
        chk.check_attr(tp, CLASS)
        self.K = getattr(tp, CLASS)

    @patch('builtins.print')
    def test_main_call_reset(self, mock_prn:callable):
        """ Apriori: does main really call reset ? """
        obj = self.K(samples[1]) # std base
        # step 2 we twist current, current_sz, candidates
        for att in "current candidates_sz candidates".split():
            chk.check_attr(obj, att)
        obj.current = {}
        candidates_sz = 42
        candidates = {}
        # step 3 we call main and see if we have the results
        chk.check_attr(obj, 'main')
        _log = obj.main(.3)
        self.assertEqual(obj.candidates_sz, 3,
                         "wrong 'candidates_sz'")
        self.assertTrue(len(obj.candidates)==2,
                        "wrong 'candidates'")
        self.assertTrue(len(obj.current)==1,
                        "wrong 'current'")

    @patch('builtins.print')
    def test_main(self, mock_prn:callable):
        """ Apriori: main should provide correct results """
        _latt = "current candidates_sz candidates support_history"
        for k in samples:
            with self.subTest(data=k):
                obj = self.K(samples[k])
                # check att
                for att in _latt.split(): chk.check_attr(obj, att)
                chk.check_attr(obj, 'main')
                for i,minsupp in enumerate((0, .5, 1)):
                    _out = obj.main(minsupp)
                    _good = resultat_main[i][k]
                    # output of main
                    self.assertTrue(_out==_good,
                                    "{} {:.2f} {}".format(k,minsupp,_out))
                    # attributes
                    for att in _latt.split():
                        if att == "support_history": continue
                        _out = getattr(obj, att)
                        _good = resultat_att[i][k].get(att, None)
                        self.assertEqual(_out,_good,
                                    "{}: {} {:.2f} {}".format(att, k,
                                                              minsupp,_out))
                        
                    
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestDefault, TestInit, TestReset, TestSupport,
               TestScan, TestLk, TestProduct, TestMain)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet
        
