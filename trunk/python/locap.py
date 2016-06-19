import tlbx

def random_db(cnctn):
    slot_list = tlbx.fetch_slot(cnctn)
    sku_id_list = tlbx.fetch_sku(cnctn,'id')
    return random(slot_list, sku_id_list)

def random(slot_list,sku_id_list):
    from random import sample
    sku_id_list_random = sample(sku_id_list,len(sku_id_list))
    for i in range(min(len(slot_list),len(sku_id_list_random))):
        slot_quantity = 5
        slot_sku_id = sku_id_list_random[i]
        slot = []
        slot_list[i].append(slot_sku_id)
        slot_list[i].append(slot_quantity)
    return slot_list

def coi_db(graph,cnctn,depot_node_id):
    line_item_sku = tlbx.fetch_line_item(cnctn,'sku_id')
    slots = tlbx.fetch_slot(cnctn)
    sku_id_list = tlbx.fetch_sku(cnctn,'id')
    return coi(graph, line_item_sku, slots, sku_id_list, depot_node_id)

def coi(graph, line_item_sku, slots, sku_id_list, depot_node_id):
    from copy import copy
    import graph
    sku_index_list = []
    for id in sku_id_list:
        sku_index = [id, line_item_sku.count(id)]
        sku_index_list.append(sku_index)
    # sorting the SKUs based on the popularity
    sku_index_list = sorted(sku_index_list, key=lambda sku_index_list: sku_index_list[2])
    # Calculating the distance of each slot to the depot
    for slot in slots:
        pick_seq = [0,slot[0]]
        distance_matrix = graph.nx_dijkstra_dm(graph,pick_seq)
        slot.append(distance_matrix[0][1])
    #Sorting the Slots based on their closeness to the depot
    slots = sorted(sku_index_list, key=lambda slots: slots[2], reverse=True)
    #assigning the top SKUs to the TOP locations till one of them ends
    for i in range(min(len(sku_index_list),len(slots))):
        del slots[i][-1]
        slots[i].append(sku_index_list[i][0])
    return slots
        