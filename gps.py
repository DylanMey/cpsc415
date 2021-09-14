#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2 template
Dylan Meyers, University of Mary Washington, fall 2021
'''

from math import inf
from atlas import Atlas
import numpy as np
import logging
import sys
from collections import defaultdict

def find_best_path(atlas):
    '''Finds the best path from src to dest, based on costs from atlas.
    Returns a tuple of two elements. The first is a list of city numbers,
    starting with 0 and ending with atlas.num_cities-1, that gives the
    optimal path between those two cities. The second is the total cost
    of that path.'''

    # THIS IS WHERE YOUR AMAZING CODE GOES
    
    num_cities = atlas.get_num_cities()
    nodes = {}
    
    number_to_add = 0
    i = 0
    while(i != num_cities-1):
        # print(i)
        dict_1 = {}
        for x in range(num_cities):

            if atlas.get_road_dist(i,x) != inf and i != x:
                dict_1["{}".format(x)] = number_to_add + atlas.get_road_dist(i,x) + atlas.get_crow_flies_dist(i,x)
                print("node being expanded")
                print(i)
                print("next possible node")
                print(x)
            if  len(dict_1) >0:
                nodes["{}".format(i)]= dict_1

            if x == num_cities-1:
                lowest_node = lowest_value(nodes)
                print(lowest_node)
                i = int(lowest_node[1])
                print(i)
                number_to_add = nodes[lowest_node[0]][lowest_node[1]]


                


    print()
    # print(nodes)

                   

            
    # print(nodes)
    # Here's a (bogus) example return value:
    return ([0,3,2,4],970)

def lowest_value(dict):
    tuple_dict = {}
   
  
    for i in dict:
       
       low =  min(dict[i], key=dict[i].get)
       tuple_dict[(i,low)] = dict[i][low]
       
    return min(tuple_dict, key=tuple_dict.get)







if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
        print("Usage: gps.py numCities|atlasFile [debugLevel].")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] not in ['DEBUG','INFO','WARNING','ERROR']:
            print('Debug level must be one of: DEBUG, INFO, WARNING, ERROR.')
            sys.exit(2)
        logging.getLogger().setLevel(sys.argv[2])
    else:
        logging.getLogger().setLevel('INFO')

    try:
        num_cities = int(sys.argv[1])
        logging.info('Building random atlas with {} cities...'.format(
            num_cities))
        usa = Atlas(num_cities)
        logging.info('...built.')
    except:
        logging.info('Loading atlas from file {}...'.format(sys.argv[1]))
        usa = Atlas.from_filename(sys.argv[1])
        logging.info('...loaded.')

    path, cost = find_best_path(usa)
    print('Best path from {} to {} costs {}: {}.'.format(0,
        usa.get_num_cities()-1, cost, path))
    print('You expanded {} nodes: {}'.format(len(usa._nodes_expanded),
        usa._nodes_expanded))

