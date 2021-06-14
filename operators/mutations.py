#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:16:24 2019

@author: RaeChen
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import random
from general import slices
from numpy.random import choice


def matrixMutation(cand,pm):
    mutant=cand.copy()
    if random()<pm:
        n,m=cand.shape
        n_slices = slices(n)
        m_slices = slices(m)
        s1 = next(n_slices) #attributes slices
        s2 = next(m_slices) #cases slices
        size=s2.stop-s2.start
        for i in range(s1.start,s1.stop):
            mutant[i,s2]=choice(cand[i],size=size,replace=True)
        return mutant
    else:
        #print("Candidate doesn't mutate")
        return mutant 
    
def uniformMutation(cand, pum):
    mutant=cand.copy()
    if pum<=1.0 and pum>=0:
        n,m=cand.shape
        for i in range(n):
            for j in range(m):
                if random()<pum:
                    mutant[i][j]=choice(cand[i],size=1,replace=True)
        return mutant
    else:
        raise ValueError('invalid pum value')