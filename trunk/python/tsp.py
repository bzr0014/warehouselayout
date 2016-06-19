# Copyright 2010-2014 Google
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Traveling Salesman Sample.
   This is a sample using the routing library python wrapper to solve a
   Traveling Salesman Problem.
   The description of the problem can be found here:
   http://en.wikipedia.org/wiki/Travelling_salesman_problem.
   The optimization engine uses local search to improve solutions, first
   solutions being generated using a cheapest addition heuristic.
   Optionally one can randomly forbid a set of random connections between nodes
   (forbidden arcs).
"""
import random
import argparse
#from ortools.constraint_solver import pywrapcp

parser = argparse.ArgumentParser()
parser.add_argument('--tsp_size', default = 50, type = int,
                    help='Size of Traveling Salesman Problem instance.')
parser.add_argument('--tsp_use_random_matrix', default=True, type=bool,
                    help='Use random cost matrix.')
parser.add_argument('--tsp_random_forbidden_connections', default = 0,
                    type = int, help='Number of random forbidden connections.')
parser.add_argument('--tsp_random_seed', default = 0, type = int,
                    help = 'Random seed.')
parser.add_argument('--light_propagation', default = False,
                    type = bool, help = 'Use light propagation')

# Cost/distance functions.

distance_matrix = []

def DistanceMatrix(i, j):
    return distance_matrix[i][j]

class RandomMatrix(object):
  """Random matrix."""

  def __init__(self, size, seed):
    """Initialize random matrix."""

    rand = random.Random()
    rand.seed(seed)
    distance_max = 100
    self.matrix = {}
    for from_node in range(size):
      self.matrix[from_node] = {}
      for to_node in range(size):
        if from_node == to_node:
          self.matrix[from_node][to_node] = 0
        else:
          self.matrix[from_node][to_node] = rand.randrange(distance_max)

  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]

def google_sku(sku_pick_seq,slots,graph,depot_node_id):
    from pickseq import sku_to_node_pick
    node_pick_seq,slot_pick_seq = sku_to_node_pick(sku_pick_seq,slots)
    return google_node(node_pick_seq,slot_pick_seq,sku_pick_seq, graph, depot_node_id)

def google_node(node_pick_seq,slot_pick_seq,sku_pick_seq, graph, depot_node_id):
    from graph import nx_dijkstra_dm
    node_pick_seq = [depot_node_id] + node_pick_seq
    dm = nx_dijkstra_dm(graph,node_pick_seq)
    return google_distance_matrix(dm,node_pick_seq,slot_pick_seq,sku_pick_seq,depot_node_id)
    
def google_distance_matrix(M,node_pick_seq,slot_pick_seq,sku_pick_seq,depot_node_id):
    global distance_matrix
    distance_matrix = M
    parser = argparse.ArgumentParser()
    parser.add_argument('--tsp_size', default = len(distance_matrix), type = int,help='Size of Traveling Salesman Problem instance.')
    parser.add_argument('--tsp_use_random_matrix', default=False, type=bool,help='Use random cost matrix.')
    parser.add_argument('--tsp_random_forbidden_connections', default = 0,type = int, help='Number of random forbidden connections.')
    parser.add_argument('--tsp_random_seed', default = 0, type = int,help = 'Random seed.')
    parser.add_argument('--light_propagation', default = False,type = bool, help = 'Use light propagation')
    args = parser.parse_args()    
  # Create routing model
    if args.tsp_size > 0:
    # Set a global parameter.
        param = pywrapcp.RoutingParameters()
        param.use_light_propagation = args.light_propagation
        pywrapcp.RoutingModel.SetGlobalParameters(param)

    # TSP of size args.tsp_size
    # Second argument = 1 to build a single tour (it's a TSP).
    # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
    # the route is node 0.
        routing = pywrapcp.RoutingModel(args.tsp_size, 1)

        parameters = pywrapcp.RoutingSearchParameters()
    # Setting first solution heuristic (cheapest addition).
        parameters.first_solution = 'PathCheapestArc'
    # Disabling Large Neighborhood Search, comment out to activate it.
        parameters.no_lns = True
        parameters.no_tsp = False

    # Setting the cost function.
    # Put a callback to the distance accessor here. The callback takes two
    # arguments (the from and to node inidices) and returns the distance between
    # these nodes.
        matrix = RandomMatrix(args.tsp_size, args.tsp_random_seed)
        matrix_callback = matrix.Distance
        if args.tsp_use_random_matrix:
            routing.SetArcCostEvaluatorOfAllVehicles(matrix_callback)
        else:
            routing.SetArcCostEvaluatorOfAllVehicles(DistanceMatrix)
    # Forbid node connections (randomly).
    ##    rand = random.Random()
    ##    rand.seed(args.tsp_random_seed)
    ##    forbidden_connections = 0
    ##    while forbidden_connections < args.tsp_random_forbidden_connections:
    ##        from_node = rand.randrange(args.tsp_size - 1)
    ##        to_node = rand.randrange(args.tsp_size - 1) + 1
    ##        if routing.NextVar(from_node).Contains(to_node):
    ##            print('Forbidding connection ' + str(from_node) + ' -> ' + str(to_node))
    ##            routing.NextVar(from_node).RemoveValue(to_node)
    ##            forbidden_connections += 1

    # Solve, returns a solution if any.
        assignment = routing.SolveWithParameters(parameters, None)
        if assignment:
         # Solution cost.
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            node = routing.Start(route_number)
            route = []
            while not routing.IsEnd(node):
                route.append(int(node))
                node = assignment.Value(routing.NextVar(node))
            result = []
            for stop in route:
                if stop==0:
                    pick = {'SKU':'Depot Node','Slot':'Depot Node','Node':depot_node_id}
                elif stop>0:
                    stop_node_id = node_pick_seq[stop-1]
                    stop_slot_id = slot_pick_seq[stop-1]
                    stop_sku_id = sku_pick_seq[stop-1]
                    pick = {'SKU':stop_sku_id,'Slot':stop_slot_id,'Node':stop_node_id}
                result.append(pick)
            return result
        else:
            print('No solution found.')
    else:
        print('Specify an instance greater than 0.')


    
    
        
def tsp_solver_master(sku_pick_seq,slots,graph,depot_node_id):
    from tsp_solver.greedy import solve_tsp
    from pickseq.py import sku_to_node_pick
    from graph.py import nx_dijkstra_dm
    global distance_matrix
    node_pick_seq = sku_to_node_pick(sku_pick_seq,slots)
    node_pick_seq = [depot_node_id] + node_pick_seq + [depot_node_id]
    distance_matrix = nx_dijkstra_dm(graph,node_pick_seq)
    route = solve_tsp(distance_matrix)
    result = []
    for stop in route:
        stop_node_id = node_pick_seq[stop]
        stop_slot_id = slot_pick_seq[stop]
        stop_sku_id = sku_pick_seq[stop]
        pick = {'SKU':stop_sku_id,'Slot':stop_slot_id,'Node':stop_node_id}
        result.append(pick)
    return result


#!/usr/bin/python
# Copyright 2015, Gurobi Optimization, Inc.

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
from gurobipy import *


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        selected = []
        # make a list of edges selected in the solution
        for i in range(n):
            sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
            selected += [(i,j) for j in range(n) if sol[j] > 0.5]
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add a subtour elimination constraint
            expr = 0
            for i in range(len(tour)):
                for j in range(i+1, len(tour)):
                    expr += model._vars[tour[i], tour[j]]
            model.cbLazy(expr <= len(tour)-1)


# Euclidean distance between two points

def distance(distance_matrix, i, j):
    return distance_matrix[i][j]


# Given a list of edges, finds the shortest subtour
def subtour(edges):
    visited = [False]*n
    cycles = []
    lengths = []
    selected = [[] for i in range(n)]
    for x,y in edges:
        selected[x].append(y)
    while True:
        current = visited.index(False)
        thiscycle = [current]
        while True:
            visited[current] = True
            neighbors = [x for x in selected[current] if not visited[x]]
            if len(neighbors) == 0:
                break
            current = neighbors[0]
            thiscycle.append(current)
        cycles.append(thiscycle)
        lengths.append(len(thiscycle))
        if sum(lengths) == n:
            break
    return cycles[lengths.index(min(lengths))]

def gurobi_sku(sku_pick_seq,slots,graph,depot_node_id):
    from pickseq import sku_to_node_pick
    node_pick_seq,slot_pick_seq = sku_to_node_pick(sku_pick_seq,slots)
    return gurobi_node(node_pick_seq,slot_pick_seq,sku_pick_seq, graph, depot_node_id)
    
def gurobi_node(node_pick_seq,slot_pick_seq,sku_pick_seq, graph, depot_node_id):
    from graph import nx_dijkstra_dm
    node_pick_seq = [depot_node_id] + node_pick_seq
    dm = nx_dijkstra_dm(graph,node_pick_seq)
    return gurobi_distance_matrix(dm,node_pick_seq,slot_pick_seq,sku_pick_seq,depot_node_id)
    
def gurobi_distance_matrix(M,node_pick_seq,slot_pick_seq,sku_pick_seq,depot_node_id):
    # Parse argument
    global distance_matrix
    distance_matrix = M
    global n 
    n = len(distance_matrix)
    m = Model() #??? it seems to be like a gurobi model constructor


# Create variables
    vars = {}
    for i in range(n):
        for j in range(i+1):
                                #obj is                                         
                                #--------------'-------------------
            vars[i,j] = m.addVar(obj=distance(distance_matrix, i, j), vtype=GRB.BINARY,
                                 name='e'+str(i)+'_'+str(j))
            #adds a variable to the gurobi model
            vars[j,i] = vars[i,j]
    m.update()


# Add degree-2 constraint, and forbid loops
    for i in range(n):
        m.addConstr(quicksum(vars[i,j] for j in range(n)) == 2)                 #A version of the Python sum function that is much more efficient 
                                                                                #for building large Gurobi expressions (LinExpr or QuadExpr objects). 
                                                                                #The function takes a list of terms as its argument. Its arguments
                                                                                #are expressions of gurobi variable types
                                                                                
        vars[i,i].ub = 0                                                        #var[i, i] should always be zero, so the upper bounds are set to be
    m.update()


# Optimize model

    m._vars = vars
    m.params.LazyConstraints = 1 #???
    m.optimize(subtourelim)      #???

    solution = m.getAttr('x', vars)
    selected = [(i,j) for i in range(n) for j in range(n) if solution[i,j] > 0.5]
    assert len(subtour(selected)) == n
    route = subtour(selected)
    result = []
    for stop in route:
        if stop==0 or stop==(len(route)-1):
            pick = {'SKU':'Depot Node','Slot':'Depot Node','Node':depot_node_id}
        elif stop>0 and stop<(len(route)-1):
            stop_node_id = node_pick_seq[stop-1]
            stop_slot_id = slot_pick_seq[stop-1]
            stop_sku_id = sku_pick_seq[stop-1]
            pick = {'SKU':stop_sku_id,'Slot':stop_slot_id,'Node':stop_node_id}
        result.append(pick)
    return result,m.objVal
    print('')
    print('Optimal tour: %s' % str(subtour(selected)))
    print('Optimal cost: %g' % m.objVal)
    print('')
    
    
    
    
    
    
    
