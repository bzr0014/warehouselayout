
def sku(sku_count):
    sku_list=[]
    for i in range(sku_count):
        sku = []
        sku_id = i+1
        sku_name = "sku{}".format(i+1)
        sku_desc = ""
        sku_class = "A"
        sku.append(sku_id)
        sku.append(sku_name)
        sku.append(sku_desc)
        sku.append(sku_class)
        sku_list.append(sku)
    return sku_list

def order_normal_datebound(avg_order_per_day,stdev,start_date,end_date,pick_date_deviation):
    from datetime import datetime
    from random import normalvariate
    start_date = datetime.toordinal(start_date)
    end_date = datetime.toordinal(end_date)
    order_list = []
    order_number = 0
    for day in range(end_date-start_date):
        today_order_count = max([int(normalvariate(avg_order_per_day,stdev)),0])
        for order in range(today_order_count):
            order = []
            order_number =order_number +1
            order_date = datetime.fromordinal(day+start_date)
            order_pick_date = datetime.fromordinal(day + start_date+pick_date_deviation)
            order_customer = "Costumer {}".format(order_number)
            order.append(order_number)
            order.append(order_date.strftime('%Y/%m/%d'))
            order.append(order_pick_date.strftime('%Y/%m/%d %X'))
            order.append(order_customer)
            order.append(order_number)
            order_list.append(order)
    return order_list

def order_datebound(order_per_day,start_date,end_date,pick_date_deviation):
    from datetime import datetime
    start_date = datetime.toordinal(start_date)
    end_date = datetime.toordinal(end_date)
    order_list = []
    order_number = 0
    for day in range(end_date-start_date):
        for order in range(order_per_day):
            order = []
            order_number =order_number +1
            order_date = datetime.fromordinal(day+start_date)
            order_pick_date = datetime.fromordinal(day + start_date+pick_date_deviation)
            order_customer = "Costumer {}".format(order_number)
            order.append(order_number)
            order.append(order_date.strftime('%Y/%m/%d'))
            order.append(order_pick_date.strftime('%Y/%m/%d %X'))
            order.append(order_customer)
            order.append(order_number)
            order_list.append(order)
    return order_list

def line_item_fixn (line_per_order,quantity,sku_id_list,order_id_list):
    from random import sample
    line_list = []
    for order in order_id_list:
        skus = sample(sku_id_list,line_per_order)
        for sku in skus:
            line = []
            line_quantity = quantity
            line_order_id = order
            line_sku_id = sku
            line.append(line_quantity)
            line.append(line_order_id)
            line.append(line_sku_id)
            line_list.append(line)
    return line_list
            
            
