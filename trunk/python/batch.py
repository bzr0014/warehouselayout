import tlbx
import networkx as nx

def order_in_one_all_db(cnctn):
    print "Creating the batch of SKUs to be picked based on the each order in one trip logic..."
    sku_batch_list = []
    order_id_list = tlbx.fetch_orders(cnctn,"id")
    line_item = tlbx.fetch_line_item(cnctn)
    for order_id in order_id_list:
        sku_batch = []
        for line in line_item:
            if line[0]==id:
                sku_batch.append(line[2])
        sku_batch_list.append(sku_batch)
    return sku_batch_list
    
def order_in_one_all(item_list,order_id_list):
    #single order pick list generator
    print "Creating the sequence of SKUs to be picked based on the each order in one trip logic..."
    sku_pick_list = []    
    for id in order_id_list:
        sku_pick = []
        for item in item_list:
           if id==item[1]:
               sku_pick.append(item[2])
        sku_pick_list.append(sku_pick)
    return sku_pick_list

def fixed_size_all_db(cnctn,batch_size):
    line_item_list = tlbx.fetch_line_item(cnctn)
    return fixed_size_all(line_item_list, batch_size)

def fixed_size_all (item_list, batch_size):
    print "Creating the sequence of SKUs to be picked based on fixed number of SKUs per trip..."
    sku_pick_list = []    
    total_assigned = 0
    while total_assigned<len(item_list):
        if len(item_list)-total_assigned<batch_size:
            batch_size = len(item_list)-total_assigned
        for i in range(batch_size):
            sku_pick = []
            sku_pick.append(item_list[total_assigned][2])
            sku_pick_list.append(sku_pick)
        total_assigned = total_assigned +1
    return sku_pick_list

def sku_to_node(sku_pick,slots):
    print "Creating a Node list from the SKU list..."
    node_pick = []
    slot_pick = []
    for sku_id in sku_pick:
        for slot in slots:
            if (len(slot)>2) and (slot[2]==sku_id):
                node_pick.append(slot[1])
                slot_pick.append(slot[0])
    return node_pick,slot_pick

def sku_to_node_db(sku_batch,cnctn):
    slots = tlbx.fetch_slot(cnctn)
    return sku_to_node(sku_batch, cnctn)