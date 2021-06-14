# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 11:50:12 2019

@author: mbgppyc3
"""

import general
from fitness.utility import full_divergence
from fitness.risk import rcap
from individual import univariate
from population import Population
import process
from operators import selections as sl
from operators import crossovers as cr
from operators import mutations as mt

ori_data, m = general.get_data('data1.csv', 1)
shape = general.unique(ori_data)
ori_full_table = general.create_array(ori_data, shape)

size=10
obj=[full_divergence, rcap]
weight=[0.5, 0.5]

'''
---------------------------------Run-------------------------------------------
'''
#Initial Population
pop=Population(ori_data, size, None)
pop.initialPopulation(m, shape, ori_full_table, [full_divergence, rcap], 
                      [0.5, 0.5], univariate)

pop.populationFitness()
divergence=min(pop.pop_fitsca)

#Loop
while divergence>=0.2:

    '''
    SELECTION
    '''
    pool=process.selection(pop, sl.tournament, False, 2)
    
    '''
    CROSSOVER
    '''
    offspring=process.crossover(pool, None, cr.uniformCrossover, pc=.3)
    
    '''
    MUTATION
    '''
    offspring=process.mutation(offspring, None, 
                       mutation_fn=mt.uniformMutation, pm=.01)
    
    '''
    NEW GENERATION
    '''
    pop=process.newPopulation(offspring, ori_data, m, shape, ori_full_table, 
                              obj, weight, size)
    
    pop.populationFitness()
    
    divergence=min(pop.pop_fitsca)




