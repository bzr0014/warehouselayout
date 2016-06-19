import math
from pyx import *

def twobyone(warehouse_width,warehouse_lengh,node_distance,center_aisle_width,bottom_aisle_width,aisle_width,aisle_angle_degree,slots_per_node):
    #Setting the depot node, and 2 main nodes above it
    depot_node = [1,"N0",0,0,0,"picker"]
    bottom_center_node = [2,"N1",depot_node[3],bottom_aisle_width/2.0,0,"picker"]
    bottom_top_node = [3,"N2",depot_node[3],bottom_aisle_width,0,"picker"]
    
    #Adding the nodes to the nodes list
    nodes = []
    nodes.append(depot_node)
    nodes.append(bottom_center_node)
    nodes.append(bottom_top_node)
    
    aisle_angle_pi = (float(aisle_angle_degree)/180)*math.pi
    
    slots = []
    #Arcs
    arcs = []
    # Creates the first to arc (from depot to the main node and from the bottom main node to top main node
    arc = [len(arcs)+1,1,depot_node[0],bottom_center_node[0]]
    arcs.append(arc)
    arc = [len(arcs)+1,1,bottom_center_node[0],bottom_top_node[0]]
    arcs.append(arc)
    
    #checks if the angle is 90 or 0
    if aisle_angle_degree==0:
        angle_factor_x = 0
    if aisle_angle_degree == 90:
        angle_factor_y = 0
    elif aisle_angle_degree<90 and aisle_angle_degree>0:
        angle_factor_y = 1/math.cos(aisle_angle_pi)
        angle_factor_x = 1/math.sin(aisle_angle_pi)

    #This case, the design is Chevron
    if aisle_angle_degree<90 and aisle_angle_degree>0:
        x_distance = node_distance*angle_factor_x
        y_distance = node_distance*angle_factor_y
        section_size = [(warehouse_lengh-center_aisle_width)/2,warehouse_width-bottom_aisle_width]
        for i in range(1,int(section_size[0]/x_distance)+1):
            if i ==1:
            #if this the first node in the aisles, it will connect it to the main nodes
                left_aisle_node = [len(nodes)+1,"N{}".format(len(nodes)),bottom_center_node[2]-(center_aisle_width/2),bottom_center_node[3],0,"picker"]
                arc = [len(arcs)+1,1,bottom_center_node[0],left_aisle_node[0]]
                arcs.append(arc)
                right_aisle_node = [len(nodes)+2,"N{}".format(len(nodes)),bottom_center_node[2]+(center_aisle_width/2),bottom_center_node[3],0,"picker"]
                arc = [len(arcs)+1,1,bottom_center_node[0],right_aisle_node[0]]
                arcs.append(arc)
            elif i>1:
                arc = [len(arcs)+1,1,left_aisle_node[0]]
                left_aisle_node = [len(nodes)+1,"N{}".format(len(nodes)),left_aisle_node[2]-(x_distance),bottom_center_node[3],0,"picker"]
                arc.append(left_aisle_node[0])
                arcs.append(arc)
                arc = [len(arcs)+1,1,right_aisle_node[0]]
                right_aisle_node = [len(nodes)+2,"N{}".format(len(nodes)),right_aisle_node[2]+(x_distance),bottom_center_node[3],0,"picker"]
                arc.append(right_aisle_node[0])
                arcs.append(arc)
            nodes.append(left_aisle_node)
            nodes.append(right_aisle_node)
            aisle_node_l = [len(nodes)+1,"N{}".format(len(nodes)),left_aisle_node[2],left_aisle_node[3]+bottom_aisle_width/2.0,0,"picker"]
            nodes.append(aisle_node_l)
            arc = [len(arcs)+1,1,left_aisle_node[0],aisle_node_l[0]]
            arcs.append(arc)
            aisle_node_r = [len(nodes)+1,"N{}".format(len(nodes)),right_aisle_node[2],right_aisle_node[3]+bottom_aisle_width/2.0,0,"picker"]
            nodes.append(aisle_node_r)
            arc = [len(arcs)+1,1,right_aisle_node[0],aisle_node_r[0]]
            arcs.append(arc)
            for j in range(1,min(int((section_size[0]+(center_aisle_width/2)-abs(aisle_node_r[2]))*angle_factor_y/(node_distance)),int((section_size[1]-abs(aisle_node_r[3]))*angle_factor_x/(node_distance)))):
                y = aisle_node_r[3] + node_distance*math.sin(aisle_angle_pi)*j
                if j ==1:
                    arc_l = [len(arcs)+1,1,aisle_node_l[0]]
                    arc_r = [len(arcs)+2,1,aisle_node_r[0]]
                elif j>1:
                    arc_l = [len(arcs)+1,1,node_l[0]]
                    arc_r = [len(arcs)+2,1,node_r[0]]
                node_r = [len(nodes)+1,"N{}".format(len(nodes)),aisle_node_r[2]+(node_distance*math.cos(aisle_angle_pi)*j),y,0,"picker"]
                nodes.append(node_r)
                node_l = [len(nodes)+1,"N{}".format(len(nodes)),aisle_node_l[2]-(node_distance*math.cos(aisle_angle_pi)*j),y,0,"picker"]
                nodes.append(node_l)
                arc_l.append(node_l[0])
                arc_r.append(node_r[0])
                arcs.append(arc_l)
                arcs.append(arc_r)
                for i in range(slots_per_node):
                    slot_r = []
                    slot_r.append(len(slots)+1)
                    slot_r.append(node_r[0])
                    slot_l = []
                    slot_l.append(len(slots)+2)
                    slot_l.append(node_l[0])
                    slots.append(slot_r)
                    slots.append(slot_l)
                    
        for i in range(1,int((warehouse_width-bottom_aisle_width)/float(y_distance))):
            if i ==1:
                arc = [len(arcs)+1,1,bottom_top_node[0]]
            elif i >1:
                arc = [len(arcs)+1,1,aisle_node[0]]
            aisle_node = [len(nodes)+1,"N{}".format(len(nodes)),bottom_top_node[2],bottom_top_node[3]+y_distance*i,0,"picker"]
            nodes.append(aisle_node)
            arc.append(aisle_node[0])
            arcs.append(arc)
            aisle_node_r = [len(nodes)+1,"N{}".format(len(nodes)),bottom_top_node[2]+center_aisle_width/2,bottom_top_node[3]+y_distance*i,0,"picker"]
            nodes.append(aisle_node_r)
            arc = [len(arcs)+1,1,aisle_node[0],aisle_node_r[0]]
            arcs.append(arc)
            aisle_node_l = [len(nodes)+1,"N{}".format(len(nodes)),bottom_top_node[2]-center_aisle_width/2,bottom_top_node[3]+y_distance*i,0,"picker"]
            nodes.append(aisle_node_l)
            arc = [len(arcs)+1,1,aisle_node[0],aisle_node_l[0]]
            arcs.append(arc)
            for j in range(1,min(int((section_size[0]+(center_aisle_width/2)-abs(aisle_node_r[2]))*angle_factor_y/(node_distance)),int((section_size[1]-abs(aisle_node_r[3]))*angle_factor_x/(node_distance)))):
                y = aisle_node_r[3] + node_distance*math.sin(aisle_angle_pi)*j
                if j ==1:
                    arc_l = [len(arcs)+1,1,aisle_node_l[0]]
                    arc_r = [len(arcs)+2,1,aisle_node_r[0]]
                elif j>1:
                    arc_l = [len(arcs)+1,1,node_l[0]]
                    arc_r = [len(arcs)+2,1,node_r[0]]
                node_r = [len(nodes)+1,"N{}".format(len(nodes)),aisle_node_r[2]+(node_distance*math.cos(aisle_angle_pi)*j),y,0,"picker"]
                nodes.append(node_r)
                node_l = [len(nodes)+1,"N{}".format(len(nodes)),aisle_node_l[2]-(node_distance*math.cos(aisle_angle_pi)*j),y,0,"picker"]
                nodes.append(node_l)
                arc_l.append(node_l[0])
                arc_r.append(node_r[0])
                arcs.append(arc_l)
                arcs.append(arc_r)
                for i in range(slots_per_node):
                    slot_r = []
                    slot_r.append(len(slots)+1)
                    slot_r.append(node_r[0])
                    slot_l = []
                    slot_l.append(len(slots)+2)
                    slot_l.append(node_l[0])
                    slots.append(slot_r)
                    slots.append(slot_l)

    return arcs,nodes,slots

def draw_whouse(arcs,nodes,slots,fname="Sample Warehouse Plan"):
    c = canvas.canvas()
    for arc in arcs:
        c.stroke(path.line(arc[2][3],arc[2][4],arc[3][3],arc[3][4]),[color.rgb.red])
    for node in nodes:
        c.fill(path.circle(node[3],node[4],1),[color.rgb.blue])
    c.writeEPSfile(fname)
    print "Warehouse drawn"
    