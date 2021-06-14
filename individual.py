# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt
import numpy as np
from numpy.random import choice
from operators.mutations import uniformMutation

'''
 Initial individuals generating functions
'''    
def uniform(data):
    return np.vstack([choice(np.unique(row),size=data.shape[1],replace=True) for row in data])

def univariate(data):
    return np.vstack([choice(row,size=data.shape[1],replace=True) for row in data])

def mutate(data, pm=.3):
    return uniformMutation(data, pm)

'''
 Scalar for fitness variable
'''
def fitSca(fit_var, weight):
    '''
   weight=weights of fitness objectives, weight=[w1,w2,w3...]
    '''
    fit_sca=0
    for i in range(len(weight)):
        fit_sca+=(weight[i]*fit_var[i])**2
    fit_sca=sqrt(fit_sca)/sqrt(len(weight))
    return fit_sca

'''
Individual class:
    Individual class stores original data, individual, m, shape, original full
    contingency table, weights of objectives, objectives, fitness variable, 
    fitness scalar.
'''
class Individual(object):
    '''
    The key features of the original data needed in the synthesizer are:
    •	Number of rows (cases)
    •	Shape of data: the shape of variables in the data. For example, if 
            the data has three variables: a binary variable, a 3-categories 
            variable and a 5-categories variable, then the shape of data will
            be (2,3,5)
    •	Full table: full contingency table of the data. It is a 
            high-dimensional table. For example, a data has three variables 
            will has a 3-dimensional table. Full table can be used to capture
            almost all statistical properties from a categorical data.
    '''
    def __init__(self, syn_data, ori_data, m, shape, ori_full_table,
                 obj, weight, fitvar=None, fitsca=None):
        '''
        full_divergence, dcap, rcap are boolean
        '''
        self.syn_data=syn_data
        self.ori_data=ori_data
        self.m=m
        self.shape=shape
        self.ori_full_table=ori_full_table
        self.obj=obj
        self.weight=weight
        
        
    def initialise(self, generator, *args):
        '''
        Initialise individual
        '''
        self.syn_data=generator(self.ori_data, *args)
        
    def evenWeights(self):
        '''
        Check if weights of objecitves matching the number of objectives 
        and normalised
        If not, correct weights
        '''
        if self.obj!=None:
            number_obj=len(self.obj)
        
            '''
            Assess if weights are in right format.
            Normalise weights
            '''
            if type(self.weight)!=list:
                self.weight=list(self.weight) 
            if self.weight==None or len(self.weight)!=number_obj: 
                self.weight=[1/number_obj]*number_obj
                #default weights are equal for all objectives
            else:
                self.weight=[value/sum(self.weight) for value in self.weight]
        
        else:
            raise ValueError('Objective is required.')
        
    '''
    Evaluate individual fitness
    '''
    def fitnessVariable(self):
        fitvar=[]
        for fun in self.obj:
            fitvar.append(fun(ori_data=self.ori_data, syn_data=self.syn_data, 
                               m=self.m, shape=self.shape, 
                               ori_full_table=self.ori_full_table))
        self.fitvar=fitvar
    
    def fitnessScalar(self):
        if self.weight==1:
            self.fitsca=self.fitvar
        else:
            self.fitsca=fitSca(self.fitvar, self.weight)
        