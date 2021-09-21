#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2 template
Dylan Meyers, University of Mary Washington, fall 2021
'''

from math import inf
from os import listxattr
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
    # print(atlas._adj_mat)
    
    num_cities = atlas.get_num_cities()
    # for i in range(num_cities):
    #     print (i)
    #     print(atlas.get_crow_flies_dist(i, num_cities-1))


    nodes = {}
    
    length = 0
    i = 0
    list_added = {}
    while(i != num_cities-1):
        # length = length + 1
        # if length > 10:
        #      break
        
        dict_1 = {}

    
        for x in range(num_cities):
            next_item = {}
            if atlas.get_road_dist(i,x) != inf and i != x and "{}".format(x) not in nodes :

                
                if "{}".format(i) not in nodes:
                    nodes["{}".format(i)] = {"{}".format(x): []}
                if "{}".format(x) not in nodes["{}".format(i)]:
                    nodes["{}".format(i)]["{}".format(x)] = []

                next_item["{}".format(x)]=(atlas.get_road_dist(i,x))
                next_item["hero"] = atlas.get_crow_flies_dist(x,num_cities-1)
                new_dict  = {}
                num = 0
                for c in list_added:
                    new_dict[c] = list_added[c]
                    num = num + 1
                    if num == len(list_added)-1:
                        break
                both_list = {**new_dict.copy(), **next_item.copy()}

                nodes["{}".format(i)]["{}".format(x)] = both_list.copy()
            if  len(dict_1) >0:
                nodes["{}".format(i)]= dict_1


            if x == num_cities-1:
                lowest_node = lowest_value(nodes)
                # print(lowest_node)
            
                if lowest_node == 0:
                    print("THERE IS NO SOLUTION")
                    return None
                i = int(lowest_node[1])

                list_added = nodes[lowest_node[0]][lowest_node[1]].copy()

                if i == num_cities-1:
                    final_list = list(nodes[lowest_node[0]][lowest_node[1]].keys())
                    final_values = list(nodes[lowest_node[0]][lowest_node[1]].values())
                    final_list.insert(0,0)
                    final_list.remove("hero")
                    return (final_list, sum(final_values))
                del nodes[lowest_node[0]][lowest_node[1]]
        if len(dict_1) == 0 and x == 0:
            break   




def lowest_value(dict):
    tuple_dict = {}
    for i in dict:
       if len(dict[i])>0:
           low =  minimum(dict[i])
           tuple_dict[(i,low)] = dict[i][low]
    
    return minimum(tuple_dict)


def minimum(dict):
    num = 0
    least = 0
    for key in dict:
        if num == 0:
            least = key
        if  sum(dict[key].values()) < sum(dict[least].values()):
            least = key
        num = num + 1

    return least







if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
       # print("Usage: gps.py numCities|atlasFile [debugLevel].")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] not in ['DEBUG','INFO','WARNING','ERROR']:
           # print('Debug level must be one of: DEBUG, INFO, WARNING, ERROR.')
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

