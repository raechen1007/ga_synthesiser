#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:03:56 2019

@author: RaeChen
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from general import slices
from general import reverse_slices
from random import random

   
def paraVarCrossover(cand1, cand2, pc, if_round=False, if_whole=False):
    if not cand1.shape==cand2.shape:
        raise ValueError("Arrays are different shapes")
    
    else:
        res1,res2=cand1.copy(), cand2.copy()
        n,m=cand1.shape
        
        if if_round==True:
            for i in range(m):
                if random()<pc:
                    if random()<0.5:
                        n_slices=slices(n)
                        s=next(n_slices)
                        res1[i][s], res2[i][s] =res2[i][s], res1[i][s].copy()
                    else:
                        print('margin')
                        n_slices=reverse_slices(n)
                        s1=next(n_slices)
                        s2=next(n_slices)
                        res1[i][s1], res2[i][s1] =res2[i][s1], res1[i][s1].copy()
                        res1[i][s2], res2[i][s2] =res2[i][s2], res1[i][s2].copy()
            return res1, res2
        
        elif if_whole==True:
            for i in range(m):
                if random()<pc:
                    res1[i], res2[i]=res2[i], res1[i].copy()
            return res1, res2
        
        else:
            for i in range(n):
                if random()<pc:
                    m_slices=slices(m)
                    s=next(m_slices)
                    res1[i][s], res2[i][s] =res2[i][s], res1[i][s].copy()
            return res1, res2

def paraCaseCrossover(cand1, cand2, pc, if_round=False, if_whole=False):
    if not cand1.shape==cand2.shape:
        raise ValueError("Arrays are different shapes")
        
    else:
        res1,res2=cand1.copy().T, cand2.copy().T
        n,m=cand1.shape #n:variable, m:cases
    
        if if_round==True:
            for i in range(m):
                if random()<pc:
                    if random()<0.5:
                        n_slices=slices(n)
                        s=next(n_slices)
                        res1[i][s], res2[i][s] =res2[i][s], res1[i][s].copy()
                    else:
                        print('margin')
                        n_slices=reverse_slices(n)
                        s1=next(n_slices)
                        s2=next(n_slices)
                        res1[i][s1], res2[i][s1] =res2[i][s1], res1[i][s1].copy()
                        res1[i][s2], res2[i][s2] =res2[i][s2], res1[i][s2].copy()
            return res1.T, res2.T
        
        elif if_whole==True:
            for i in range(m):
                if random()<pc:
                    res1[i], res2[i]=res2[i], res1[i].copy()
            return res1.T, res2.T
        
        else:
            for i in range(m):
                if random()<pc:
                    n_slices=slices(n)
                    s=next(n_slices)
                    res1[i][s], res2[i][s] =res2[i][s], res1[i][s].copy()
            return res1.T, res2.T
        
def matrixCrossover(cand1, cand2, pc):
    if not cand1.shape==cand2.shape:
        raise ValueError("Arrays are different shapes")
    else:
        res1, res2 = cand1.copy(), cand2.copy()
        if random()<pc:
            n,m=cand1.shape
            n_slices = slices(n)
            m_slices = slices(m)
            s1 = next(n_slices)
            s2 = next(m_slices)
            res1[s1, s2], res2[s1, s2] = res2[s1, s2], res1[s1, s2].copy()
            return res1, res2
        else:
            return res1, res2
    
def uniformCrossover(cand1, cand2, puc):
    if cand1.shape==cand2.shape and puc<=1.0 and puc>=0:
        n,m=cand1.shape
        res1, res2 = cand1.copy(), cand2.copy()
        for i in range(n):
            for j in range(m):
                if random()<puc:
                    res1[i][j], res2[i][j]=res2[i][j], res1[i][j]
        return res1, res2
    else:
        raise ValueError ('Iput Error')
        
