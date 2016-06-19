import networkx as nx
from tlbx import *
import math
try:
    import matplotlib.pyplot as plt
except:
    raise

def nx_create (arcs,nodes,graph_type):
    G = nx.Graph()
    G = nx_populate(arcs,nodes,graph_type)
    print "NetworkX graph created"
    return G

def nx_create_db(cnctn,graph_type):
    arcs = fetch_arc(cnctn)
    nodes = fetch_node(cnctn)
    return nx_create(arcs,nodes,graph_type)

def nx_populate(arcs,nodes,graph_type):
#This function creates the graph from the database node and arc table
    if graph_type[0]=="D" or graph_type[0]=="d":
        G = nx.DiGraph()
    if graph_type[0] == "U" or graph_type[0]=="u":
        G = nx.Graph()
    #adds the nodes into the graph. name, type, x,y,z of the node are added to the graph as attributes o the node 
    for node in nodes:
        G.add_node('{}'.format(node[0]),{'name':str(node[1]),'x':float(node[2]),'y':float(node[3]),'z':float(node[4]),'type':str(node[5])})
    #Adds the arcs into the graph. id, and travel factor of each arc is added as an attribute of each arc in the graph
    xLocations = nx.get_node_attributes(G, 'x')
    yLocations = nx.get_node_attributes(G, 'y')
    for arc in arcs:
        arcLenght = math.sqrt((math.pow((xLocations[str(arc[2])] - xLocations[str(arc[3])]),2) + math.pow((yLocations[str(arc[2])] - yLocations[str(arc[3])]),2)))
        G.add_edge('{}'.format(arc[2]),'{}'.format(arc[3]),{'id':str(arc[0]),'travelFactor':float(arc[1]),'length':arcLenght})   
    return G
#return the populated graph

def nx_dijkstra_dm(Graph,PickSeq):
# Creates the distance matrix from graph and a list of nodes that should be visited
    distanceMatrix = []
    for i in range(len(PickSeq)):
        distanceMatrix.append([])
        for j in range(len(PickSeq)):
            #add a step to jump over when the from and to node are the same
            #distance = nx.shortest_path_length(Graph,PickSeq[i],PickSeq[j],'length')
            distance,path = nx.bidirectional_dijkstra(Graph,str(PickSeq[i]),str(PickSeq[j]),'length')
            distanceMatrix[i].append(int(distance))
    return distanceMatrix
    # Returns the distance matrix of of the list fed to the function  

def nx_get_node_position(G):
#This function gets the positions of the nodes from the graph using the nodes x and y attribute
    posList = []
    for node in G.nodes(data=True):
        posList.append(('{}'.format(node[0]),(float(node[1]['x']),float(node[1]['y']))))
    pos = dict(posList)
    return pos
    #Returns the list of dictionaries of the positions of all the nodes in the graph

def nx_draw_graph(G,name="Graph Visual",format="png",resolution=600):
    # write the graph in a .gml file 
    nx.write_gml(G,"{}.gml".format(name))
    #Create a sample pick sequence to solve with Google_TSP
    posDic = nx_get_node_position(G)
    # positions the graph based on the position of the nodes
    position=nx.spring_layout(G,pos=posDic,fixed=posDic.keys())
    #draws the nodes of the graph using the position object
    nx.draw_networkx_nodes(G,position,node_size=10)
    #draws the edges using the position object
    nx.draw_networkx_edges(G,position,width=2)
    #sets the labels of a plot for a G graph with the defined position object
    nx.draw_networkx_labels(G,position)
    plt.axis('off')
    #saves the plot in a .png file
    plt.savefig("{}.{}".format(name,format), dpi=resolution) # save as png
    plt.show()# display