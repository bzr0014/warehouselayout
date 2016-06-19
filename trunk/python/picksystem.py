import graph
import whousedesign
import locap
import generator
import pickseq
import tsp
import tlbx
from datetime import datetime


def main():
    warehouse_width = 200
    warehouse_lengh = 400
    node_distance = 10
    center_aisle_width = 20
    bottom_aisle_width = 15
    aisle_width = 10
    aisle_angle_degree = 60
    slots_per_node = 10
    
    #starting the database
    tlbx.run_sql('./tables.sql');
    #Creating the SKU list and uploading it
    sku_list = generator.sku(5000)
    tlbx.upload_sku_to_database(sku_list)
    
    #Creating the order list and uploading it
    start_date = datetime.fromordinal(735500)
    end_date = datetime.fromordinal(735850)
    avg_order_per_day = 10
    pick_date_deviation = 3
    order_list = generator.order_normal_datebound(avg_order_per_day,3,start_date,end_date,pick_date_deviation)
    tlbx.upload_order_to_database(order_list)
    
    #Creating the item list and uploading it
    sku_id_list = [sku[0] for sku in sku_list]
    order_id_list = [order[0] for order in order_list]
    item_list = generator.line_item_fixn (5,3,sku_id_list,order_id_list)
    tlbx.upload_item_to_database(item_list)
    
    #creating a 2by1 warehouse with the specified parameters and getting the matrices of nodes, arcs, and slots
    arc_list,node_list,slot_list = whousedesign.twobyone(warehouse_width,warehouse_lengh,node_distance,center_aisle_width,bottom_aisle_width,aisle_width,aisle_angle_degree,slots_per_node)
    tlbx.upload_whouse_to_database(arc_list,node_list,slot_list)
    #whousedesign.draw_whouse(arc_list,node_list,slot_list)
    #Drawing the warehouse based on the nodes, arcs, and slots table
    
    #Updating the Slot list based on the Location Assigning Problem (LocAP)
    slot_list = locap.random(slot_list,sku_id_list)
    tlbx.upload_slot_to_database(slot_list)
    
    #Creating the Graph and visualizing it
    G = graph.nx_create(arc_list,node_list,"Undirected")
    graph.nx_draw_graph(G)
    
    #Creating the SKU pick list and later transform the list into the pick node list
    #sku_pick_list = pickseq.order_in_one_all(item_list,order_list)
    sku_pick_list = pickseq.order_in_one_all_from_db()
    #change to visitation
    depot_node_id = 1
    for sku_pick in sku_pick_list:
        #route = tsp.google_sku(sku_pick,slot_list,G,depot_node_id)
        route,obj_value = tsp.gurobi_sku(sku_pick,slot_list,G,depot_node_id)
        print route
        print obj_value

    print "All Done!"
    
if __name__ == "__main__":
    main()
