#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Ulrich ODJO && Augusta Mwinja Kachungunu"
__date__ = "03.03.23"
__usage__ = "apriori class"
__update__ = ""

class Apriori(object):
  def __init__(self, dbase: dict):
    """
    Constructor class, use to initialize attribute
    """
    self.dbase = dbase
    self.reset()

  def reset(self):
    self.candidates_sz = 1

    self.candidates = {}
    for key, val in self.dbase.items():
      self.candidates[key] = [(i,) for i in val]

    self.current = {}
    for key, val in self.candidates.items():
      for itemset in val:
        if itemset in self.current:
          self.current[itemset].add(key)
        else:
          self.current[itemset] = set([key])

    self.support_history = {}

  def support(self, prob: float) -> dict:
    items_support = {}
    for key, val in self.current.items():
      sup_prob = len(val) / len(self.dbase.keys())
      if sup_prob >= prob:
        items_support[key] = sup_prob
    return items_support

  def scan_dbase(self, prob: float):
    sup_min = self.support(prob)
    self.support_history.update(sup_min)
    self.current = {key: self.current[key] for key in sup_min.keys()}

  def Lk(self) -> list:
   current_key = list(self.current.keys())
   return sorted(current_key)

  def __update_current_candidates(self, data: dict):
    # update current with futur
    self.current = data
    # update candidates
    self.candidates = {}
    for key, val in self.current.items():
      for tid in val:
        if tid in self.candidates:
          self.candidates[tid].append(key)
        else:
          self.candidates[tid] = [key]
    # update candidates_sz
    # self.candidates_sz = len(list(data.keys())[0])
    self.candidates_sz += 1
 
  def cross_product(self):
    key_current  = self.Lk() # Lk
    itemset_size = len(key_current[0]) # k
    itemset_lenght = len(key_current) # p
    futur = {}
    
    for i in range(itemset_lenght-1):
      j = i + 1
      while (j < itemset_lenght and key_current[i][:-1] == 
             key_current[j][:-1]):
           #new = tuple(list(key_current[i])+[key_current[j][-1]])
           new = key_current[i]+key_current[j][-1:]
           if all([new[:p] + new[p+1:] in key_current
                  for p in range(len(new))]):
             futur[new] = (self.current[key_current[i]]
                           .intersection(self.current[key_current[j]]))
           j = j + 1
    self.__update_current_candidates(futur)

  def main(self, prob: float) -> list:
    self.reset()
    itemset = []
    while len(self.current) > 1:
      self.scan_dbase(prob)
      Lk = self.Lk()
      if Lk != []:
        self.cross_product()
        itemset.append(Lk)

    self.scan_dbase(prob)
    Lk = self.Lk()
    if Lk != []:
      itemset.append(Lk)
    return itemset

if __name__ == "__main__":
  dbase = {100: [1, 3, 4], 200: [2, 3, 5], 300: [1, 2, 3, 5], 400: [2, 5]}
  db = Apriori(dbase)  
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