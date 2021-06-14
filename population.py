#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:19:14 2019

@author: RaeChen
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from individual import Individual

'''
    Load syn_data from file
'''

def synthesiser(ini_file, size): #initial population loaded from csv file function
    ini=pd.read_csv(ini_file,header=None)
    ini_arr=np.array(ini)
    size=ini_arr.shape[1]
    population=np.array_split(ini_arr, size)
    for i in range(size):
        population[i]=population[i].T
    return population



'''
Population class：
    Population class store original data, population size, candidates, fitness variable
    and fitness values.
    Population_fitness() output fitness variables and values for candidates.
'''
class Population(object):
    def __init__(self, ori_data, size, candidates, pop_fitvar=None, 
                 pop_fitsca=None):
        self.ori_data=ori_data
        self.size=size
        self.candidates=candidates #candiates is list of Individual classes
        
    def initialPopulation(self, m, shape, ori_full_table, obj, weight, 
                           generator, *args):
        
        candidates=[]
        for i in range(self.size):
            ind=Individual(0, self.ori_data, m, shape, 
                                         ori_full_table, obj, weight)
            ind.initialise(generator, *args)
            candidates.append(ind)
            
        self.candidates=candidates
        
            
    def loadPopulation(self):
        #loading initial population from files
        if self.candidates==None:
            ini_file=input('Name of file:')
            self.candidates=synthesiser(ini_file, self.size)
        
        else:
            answer=input("Are you going to reset current population? Y/N")
            if answer=='Y':
                ini_file=input('Name of file:')
                self.candidates=synthesiser(ini_file, self.size)
    
    def populationFitness(self):
        '''
        Population fitness: record list of fitness variables for candidates and
        list of fitness values for candidates in the population.
        
        Can be used as evaluation of GA progress.
        '''
        
        self.pop_fitvar=[]
        self.pop_fitsca=[]
        
        for ind in self.candidates:
            ind.evenWeights() #make sure ind.weight is in right format
            ind.fitnessVariable()
            ind.fitnessScalar()
            
            #list of fitness variable of the population
            self.pop_fitvar.append(ind.fitvar)
            #list of fitness scalar of the population
            self.pop_fitsca.append(ind.fitsca)
            
            
        
        