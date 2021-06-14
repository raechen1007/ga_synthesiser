#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:13:26 2019

@author: RaeChen
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from general import psi_trans
from random import sample
import numpy as np
from math import sqrt
'''
------------------------------Selection functions------------------------------
'''
    
def tournament(fit_val, k):
   selection = []
   for _ in range(len(fit_val)):
       cands = sample(fit_val, k)
       fittest = min(cands)
       index = fit_val.index(fittest)
       selection.append(index)
   return selection
   
def linear_ranking(fit_val, etaminu, etaplus):
    n=len(fit_val) 
    ef=[] 
    pr=[]  
    ranking=sorted(range(n), key=lambda k: fit_val[k],reverse=True)
    for j in range(n):
        ef.append(etaminu+(etaplus-etaminu)*((j)/(n-1)))
        pr.append(ef[j]/n)
    selection=np.random.choice(ranking,size=n,replace=True, p=pr)
    return selection

def exp_ranking (fit_val, c):
    c=float(c)
    if c>0 and c<1:
        n=len(fit_val)
        '''coeff=(c-1)/(c**n-1)'''
        s=sum(c**(n-j) for j in range(n))
        ranking=sorted(range(n), key=lambda k: fit_val[k],reverse=True)
        pr=[]
        for i in range(n):
            '''pr.append(coeff*c**(n-ranking[i]))'''
            pr.append((c**(n-i))/s)
        selection=np.random.choice(ranking,size=n,replace=True, p=pr)
        return selection, pr
    else:
        raise ValueError('Unexpected c value')
   
def np_tournament(fit_var, size_comparison, delta):
    n=len(fit_var) #fit_var=list of tuples for multi-objective fitnesses
    
    selection=[]
    while len(selection)<n:
        competitors=sample(range(n), 2) #two candidates are picked randomly with fit_var
        remain=[x for x in range(n) if x not in competitors]
        comparison_set=sample(remain, size_comparison)
        
        '''dominated tournament'''
        count_win, count_niche=[0,0], [0,0]
        for candidate in comparison_set:
            if fit_var[competitors[0]][0]<fit_var[candidate][0] and fit_var[competitors[0]][1]<fit_var[candidate][1]:
                count_win[0]+=1
            if fit_var[competitors[1]][0]<fit_var[candidate][0] and fit_var[competitors[1]][1]<fit_var[candidate][1]:
                count_win[1]+=1
            
        '''non-dominated tournament'''
        for i in range(n):
            d_0=sqrt((fit_var[competitors[0]][0]-fit_var[0][0])**2+(fit_var[competitors[0]][1]-fit_var[0][1])**2)
            d_1=sqrt((fit_var[competitors[1]][0]-fit_var[1][0])**2+(fit_var[competitors[1]][1]-fit_var[1][1])**2)
            if d_0<=delta:
                count_niche[0]+=1
            if d_1<=delta:
                count_niche[1]+=1
            
        if max(count_win) == size_comparison and count_win[0] != count_win[1]:
            selection.append(competitors[count_win.index(max(count_win))])
        else: selection.append(competitors[count_niche.index(min(count_niche))])
        
    return selection

def stochastic_universal(fit_val): 
    fit_val=psi_trans(fit_val) #value transfered by substracting from 1.0
    n=len(fit_val)
    m=np.mean(fit_val)
    pr=[]
    for i in range(n):
        pr.append(fit_val[i]/(n*m))
    selection=list(np.random.choice(range(n),size=n,replace=True,p=pr))
    return selection, pr

def roulette_wheel(fit_val):
    fit_val=psi_trans(fit_val) #value transfered by substracting from 1.0
   
    n=len(fit_val)
    gap=1.0/n #The gap between each pointer
    order=sorted(range(n), key=lambda k: fit_val[k]) #The order of fit_val values in ascending
    partition=sorted([f/sum(fit_val) for f in fit_val])
    cmfit=list(np.cumsum(partition))
    cmfit.insert(0, 0.0) #The wheel
    
    #index of cmfit=index of sorted fit_val
    pointer=np.random.uniform(0,1,1)[0]
    pointers=[]
    for i in range(n):
        pointers.append(pointer+i*gap)
        if pointers[i]>1.0:
            pointers[i]=pointers[i]-1.0
    
    pointers=sorted(pointers)
    selection_cmfit=[]
    for x in pointers:
        j=0
        while j<=n:
            if x>cmfit[j] and x<=cmfit[j+1]:
                selection_cmfit.append(j)
                j+=1
            else:
                j+=1
    selection=[order[k] for k in selection_cmfit]
    return selection
