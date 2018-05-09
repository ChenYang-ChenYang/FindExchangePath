import os
import math
import numpy as np
from numpy import float32, int32

"""
author: Chen Yang
email: garychenyang@gmail.com
"""

price_file_path = "./latest_price.txt"

def generate_graph():
    """ generate exchange rate graph from the latest prices """
    is_first_vertex = True
    vertex_list = []
    
    if not os.path.exists(price_file_path):
        raise ValueError("There is no usable price information for exchange request, please provide firstly.")
    
    # loop each price string to create graph
    with open(price_file_path, "r") as lines:
        # get price details
        for line in lines:
            price_split = line.split(" ")
            exchange = price_split[1]
            source_currency = price_split[2]
            dest_currency = price_split[3]
            forward_factor = price_split[4]
            backward_factor = price_split[5]
            backward_factor = backward_factor[:-1]
            # initialize graph matrix 
            if(is_first_vertex):
                graph = np.array([[1, forward_factor],[backward_factor, 1]])
                # save/add exchange_currency vertex to list
                vertex_list.append(exchange+"_"+source_currency)
                vertex_list.append(exchange+"_"+dest_currency)
                is_first_vertex = False
            else:
                new_row_for_source_currency = []
                new_row_for_dest_currency = []
                new_col_for_source_currency = []
                new_col_for_dest_currency = []
                count = 0
                # loop each vertex to add edge weight for new vertex
                for vertex in vertex_list:
                    temp_currency = vertex.split("_")[1]
                    count +=1
                    # set weight to 1 if currency are the same, or set it to -1 which means there is no connection 
                    if(source_currency == temp_currency):
                        new_row_for_source_currency.append(1.0)
                        new_col_for_source_currency.append(1.0)
                    else:
                        new_row_for_source_currency.append(-math.inf)
                        new_col_for_source_currency.append(-math.inf)
                    if(dest_currency == temp_currency):
                        new_row_for_dest_currency.append(1.0)
                        new_col_for_dest_currency.append(1.0)
                    else:
                        new_row_for_dest_currency.append(-math.inf)
                        new_col_for_dest_currency.append(-math.inf)
                # transfer list to array
                new_col_for_source_currency_array = np.asarray(new_col_for_source_currency).reshape(count, 1)
                new_col_for_dest_currency_array = np.asarray(new_col_for_dest_currency).reshape(count, 1)
                # append column to existing graph matrix
                graph = np.append(graph, new_col_for_source_currency_array, axis=1)  
                graph = np.append(graph, new_col_for_dest_currency_array, axis=1)
                
                # self source to source
                new_row_for_source_currency.append(1.0)
                # self source to dest
                new_row_for_source_currency.append(forward_factor)  
                # self dest to source 
                new_row_for_dest_currency.append(backward_factor)
                # self dest to dest
                new_row_for_dest_currency.append(1.0)
                # transfer list to array
                new_row_for_source_currency_array = np.asarray(new_row_for_source_currency).reshape(1, count+2)
                new_row_for_dest_currency_array = np.asarray(new_row_for_dest_currency).reshape(1, count+2)
                # append row ot existing graph matrix
                graph = np.append(graph, new_row_for_source_currency_array, axis=0)
                graph = np.append(graph, new_row_for_dest_currency_array, axis=0)
                
                # save/add exchange_currency vertex to list
                vertex_list.append(exchange+"_"+source_currency)
                vertex_list.append(exchange+"_"+dest_currency)
    return vertex_list, graph

def find_exchange_path(vertex_list, exchange_graph, source_exchance, source_currency, dest_exchange, dest_currency):
    """ find the best exchange rate from graph by the source exchange, source currency, destination exchange and destination currency  
    
    Arguments:
    vertex_list -- vertex list, each element format is exchange_currency
    exchange_graph -- exchange graph generated from price
    source_exchance -- source exchange
    source_currency -- source currency
    dest_exchange -- destination exchange
    dest_currency -- destination currency
    
    exchange path and final rate will be returned
    """
    # initialize rate matrix, the same value with exchange graph
    rate = exchange_graph.astype(float32)
    # initialize next path matrix with 0 value, will update later
    next = np.zeros(exchange_graph.shape, dtype=int32)
    vertex_count = len(vertex_list)
    # update next matrix to set init value
    for i in range(vertex_count):
        for j in range(vertex_count):
            next[i][j] = j
    # update next matrix by rate comparison
    for k in range(vertex_count):
        for i in range(vertex_count): 
            for j in range(vertex_count):
                temp_rate = rate[i][k] * rate[k][j]
                if rate[i][j] < temp_rate and temp_rate != math.inf:
                    rate[i][j] = temp_rate
                    next[i][j] = next[i][k]
    # define a list to save final path
    path = []
    # get the index of source vertex and destination vertex
    source_index = vertex_list.index(source_exchance+"_"+source_currency)
    dest_index = vertex_list.index(dest_exchange+"_"+dest_currency)
    if next[source_index][dest_index] == None:
        return path
    path.append(source_index)
    while source_index != dest_index:
        source_index = next[source_index][dest_index]
        # It will loop infinitely if price is set unreasonably, handle the case here. Exit and return null.
        if source_index in path:
            path = []
            break
        else:
            path.append(source_index)
    return path, rate    