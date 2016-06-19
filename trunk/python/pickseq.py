import tlbx
import networkx as nx

'''
this module provides various algoriths for batching
typical parameters include:
	item_list (list) [quantity, order_id, sku_id]
	order_list (list) (id, order_dtg, target_pick_dtg , customer, order_number)
	batch_size (int)

outputs:
	sku_pickList (list[]) : a list of list of sku_ids to be picked in a single
'''

def order_in_one_all(item_list,order_list):
    #single order pick list generator
    print "Creating the sequence of SKUs to be picked based on the each order in one trip logic..."
    sku_pick_list = []    
    for order in order_list:
        sku_pick = []
        for item in item_list:
           if order[0]==item[1]:
               sku_pick.append(item[2])
        sku_pick_list.append(sku_pick)
    return sku_pick_list

def order_in_one_all_from_db():
	connection = tlbx.connection()
	cursor = connection.cursor()
	query = 'select distinct id from orders, line_item where line_item.order_id = orders.id'
	cursor.execute(query)
	order_id_list = []
	for row in cursor:
		order_id_list.append(row[0])
	sku_pick_list = []
	for order_id in order_id_list:
		query = 'select orders.id, sku_id from line_item,  orders where line_item.order_id = orders.id and orders.id = {}'.format(order_id)
		cursor.execute(query)
		sku_pick = []
		for item in cursor:
			sku_pick.append(item[1])
		sku_pick_list.append(sku_pick)
	for item in sku_pick_list:
		print item	
	return sku_pick_list
		
		

def fixed_batch_size_all (item_list, batch_size):
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

def fixed_batch_size_all_from_database (batch_size):
    print "Creating the sequence of SKUs to be picked based on fixed number of SKUs per trip..."
    connection = tlbx.connection()
    cursor = connection.cursor()
    cursor.execute('select * from line_item')
    item_list = []
    for row in cursor:
        print row
        item_list.append(row)
    sku_pick_list = []
    total_assigned = 0
    while total_assigned<len(item_list):
        if len(item_list)-total_assigned<batch_size:
            batch_size = len(item_list)-total_assigned
        sku_pick = []
        for i in range(batch_size):
            sku_pick.append(item_list[total_assigned][2])
            total_assigned = total_assigned + 1
        sku_pick_list.append(sku_pick)
    for item in sku_pick_list:
        print item
    return sku_pick_list

def sku_to_node_pick(sku_pick,slots):
    print "Creating a Node list from the SKU list..."
    node_pick = []
    slot_pick = []
    for sku_id in sku_pick:
        for slot in slots:
            if (len(slot)>2) and (slot[2]==sku_id):
                node_pick.append(slot[1])
                slot_pick.append(slot[0])
    return node_pick,slot_pick

def sku_to_node_pick_from_db(sku_pick,slots):
    print "Creating a Node list from the SKU list..."
    connection = tlbx.connection()
    cursor = connection.cursor()
    cursor.execute('select * from slot')
    slots = []
    for row in cursor:
        slots.append[row]
    node_pick = []
    slot_pick = []
    for sku_id in sku_pick:
         query = 'select * from slot where sku_id = {}'.format(sku_id)
         cursor.execute(query)
         for row in cursor:
             node_pick.append(row[1])
             slot_pick.append(row[0])
    return node_pick,slot_pick

    
