drop table if exists slot;
drop table if exists arc;
drop table if exists node;
drop table if exists line_item;
drop table if exists orders;
drop table if exists sku;


create table sku(
id int,
name varchar(50),
description varchar(255),
class enum('A', 'B', 'C', 'D'), #???
x_size float,
y_size float,
z_size float,
primary key(id)
);

create table orders(
id int,
order_dtg datetime,
target_pick_dtg datetime,
customer varchar(255),
order_number varchar(50),
order_status enum('Received', 'Picking', 'Packing', 'Shipped'),
pick_dtg datetime,
primary key (id)
);

create table line_item(
quantity int,
order_id int,
sku_id int,
status enum('Received', 'Picking', 'Packing', 'Shipped'),
foreign key (order_id) references orders(id) ON DELETE CASCADE,
foreign key (sku_id) references sku(id) ON DELETE CASCADE,
primary key (order_id, sku_id) #???
);

create table node(
id int,
name varchar(50),
x decimal(10, 2),
y decimal(10, 2),
z decimal(10, 2),
type enum('Picker', 'Input', 'Output', 'Other'),
primary key(id)
);

create table arc(
id int, 
travel_factor decimal,
head_node_id int,
tail_node_id int,
primary key(id),
foreign key(head_node_id) references node(id) ON DELETE CASCADE,
foreign key(tail_node_id) references node(id) ON DELETE CASCADE,
unique (head_node_id, tail_node_id)
);

create table slot(
id int,
node_id int,
sku_id int,
quantity mediumint,
primary key (id),
foreign key (sku_id) references sku(id) ON DELETE CASCADE,
foreign key (node_id) references node(id) ON DELETE CASCADE
);