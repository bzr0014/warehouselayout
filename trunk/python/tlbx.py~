from pyx import *
import sys
import mysql.connector
import math

def connection(user="root", password="", host="localhost", database="picksystem_nt"):
    cnctn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    return cnctn

def run_sql(path):
	cnx = connection()
	cursor = cnx.cursor()
	file = open(path, 'r')
	query = ""
	for line in file:
		query = query + line
		if line.find(';') > 0:
			#print query
			cursor.execute(query)
			query = ""

def upload_slot_to_database(slot_list):
    cnx = connection()
    cursor = cnx.cursor()
    print "Uploading Updated Slots..."
    query = ("DELETE  FROM picksystem_nt.slot;")
    cursor.execute(query)
    for slot in slot_list:
        if len(slot)==4:
            query = ("INSERT INTO picksystem_nt.slot (id, quantity, node_id, sku_id) VALUES({}, {}, {}, {});".format(slot[0],slot[3],slot[1],slot[2]))
        elif len(slot)==2:
            query = ("INSERT INTO picksystem_nt.slot (id, node_id) VALUES({}, {});".format(slot[0],slot[1]))
        cursor.execute(query)
    cnx.commit()
    cursor.close()
    
def upload_sku_to_database(sku_list):
    cnx = connection()
    cursor = cnx.cursor()
    print "Uploading SKUs..."
    query = ("DELETE  FROM picksystem_nt.sku;")
    cursor.execute(query)
    for sku in sku_list:
        query = ("INSERT INTO picksystem_nt.sku (id, name, description, class) VALUES({},'{}', '{}', '{}');".format(sku[0],sku[1],sku[2],sku[3]))
        cursor.execute(query)
    cnx.commit()
    cursor.close()
    
def upload_item_to_database(item_list):
    cnx = connection()
    cursor = cnx.cursor()
    print "Uploading Items..."
    query = ("DELETE  FROM picksystem_nt.line_item;")
    cursor.execute(query)
    for item in item_list:
	#print item
        query = ("INSERT INTO picksystem_nt.line_item (quantity, order_id, sku_id) VALUES({}, {}, {});".format(item[0],item[1],item[2]))
        cursor.execute(query)
    cnx.commit()
    cursor.close()

def upload_order_to_database(order_list):
    cnx = connection()
    cursor = cnx.cursor()
    print "Uploading Orders..."
    query = ("DELETE  FROM picksystem_nt.orders;")
    cursor.execute(query)
    for order in order_list:
        query = ("INSERT INTO picksystem_nt.orders (id, order_dtg, target_pick_dtg , customer, order_number) VALUES({},'{}', '{}', '{}','{}');".format(order[0],order[1],order[2],order[3],order[4]))
        cursor.execute(query)
    cnx.commit()
    cursor.close()
    
def upload_whouse_to_database(arcs,nodes,slots):
    cnx = connection()
    cursor = cnx.cursor()
    
    print "Uploading Nodes..."
    query = ("DELETE  FROM picksystem_nt.node;")
    cursor.execute(query)
    for node in nodes:
        query = ("INSERT INTO picksystem_nt.node (id, name, x, y, z, type) VALUES({}, '{}', {}, {}, {}, '{}');".format(node[0],node[1],node[2],node[3],node[4],node[5]))
        cursor.execute(query)
    cnx.commit()
    
    print "Uploading Arcs..."
    query = ("DELETE  FROM picksystem_nt.arc;")
    cursor.execute(query)
    for arc in arcs:
        query = ("INSERT INTO picksystem_nt.arc (id,travel_factor,head_node_id,tail_node_id) VALUES({}, {}, {}, {});".format(arc[0],arc[1],arc[2],arc[3]))
        cursor.execute(query)
    cnx.commit()
    
    print "Uploading Slots..."
    query = ("DELETE  FROM picksystem_nt.slot;")
    cursor.execute(query)
    for slot in slots:
        query = ("INSERT INTO picksystem_nt.slot (id, node_id) VALUES({}, {});".format(slot[0],slot[1]))
        cursor.execute(query)
    cnx.commit()
    cursor.close()
  
def fetch_one(cnctn,query):
    cursor = cnctn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    return data

def fetch_node(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM node;".format(to_be_fetched))
    data = cursor.fetchall()
    return data

def fetch_arc(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM arc;".format(to_be_fetched))
    data = cursor.fetchall()
    return data

def fetch_slot(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM slot;".format(to_be_fetched))
    data = cursor.fetchall()
    return data

def fetch_orders(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM orders;".format(to_be_fetched))
    data = cursor.fetchall()
    return data

def fetch_line_item(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM line_item;".format(to_be_fetched))
    data = cursor.fetchall()
    return data

def fetch_sku(cnctn,to_be_fetched="*"):
    cursor = cnctn.cursor()
    cursor.execute("SELECT {} FROM sku;".format(to_be_fetched))
    data = cursor.fetchall()
    return data
