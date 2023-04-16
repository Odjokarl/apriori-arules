#! /usr/bin/env python3
# -*-coding: utf-8 -*-

from apriori import Apriori

# Create an instance of Apriori class
data = {100:[1, 3, 4], 200:[2, 3, 5], 300:[1, 2, 3, 5], 400:[2, 5]}
db = Apriori(data)

# First block test contructor and reset method
print("dbase", db.dbase)
print("candidates_sz", db.candidates_sz)
print("support_history", db.support_history)
print("candidates", db.candidates)
print("current", db.current)

# Second block test support method
print("support(.7)", db.support(.7))
print("support(.2)", db.support(.2))

# Third block test scan_dbase method
print("#{}#".format('='*73))
db.scan_dbase(.7)
print("support_history", db.support_history)
print("current", db.current)

# Fourth block test Lk method
print("Lk for size {}".format(db.candidates_sz), db.Lk())

# Fith block of code
print("dbase", db.dbase)
print("candidates_sz", db.candidates_sz)
print("support_history", db.support_history)
print("candidates", db.candidates)
print("current", db.current)
print("support(.7)", db.support(.7))
print("support(.2)", db.support(.2))
print("#{}#".format('='*73))
db.scan_dbase(.7)
print("support_history", db.support_history)
print("current", db.current)
print("Lk for size {}".format(db.candidates_sz), db.Lk())
print("#{}#".format('='*73))
db.cross_product()
print("dbase", db.dbase)
print("candidates_sz", db.candidates_sz)
print("support_history", db.support_history)
print("candidates", db.candidates)
print("current", db.current)

# Sixth block of code
print("dbase", db.dbase)
print("candidates_sz", db.candidates_sz)
print("support_history", db.support_history)
print("candidates", db.candidates)
print("current", db.current)
print("main(.3)", db.main(.3))
print("candidates_sz", db.candidates_sz)
print("support_history", db.support_history)
print("candidates", db.candidates)
print("current", db.current)