package warehouslayout;

import java.util.ArrayList;
import java.sql.Date;
import java.util.HashMap;

public class PickSystem {
	public static void main(String[] args) {
		int warehouse_width = 200;
		int warehouse_length = 400;
		int node_distance = 10;
		int center_aisle_width = 20;
		int bottom_aisle_width = 15;
		int aisle_width = 10;
		int aisle_angle_degree = 60;
		int slots_per_node = 10;
		Toolbox tlbx = new Toolbox("root", "", "localhost", "picksystem_nt");
		//tlbx.run_sql("/home/behnam/warehouselayout/trunk/python/tables.sql");
		DatabaseObject sku_list = Generator.sku(5000);
		tlbx.uploadToDatabase(sku_list, "sku");
		Date start_date = new Date(735500 * Toolbox.MILISECONDS_IN_DAY);
		Date end_date = new Date(735850 * Toolbox.MILISECONDS_IN_DAY);
		int avg_order_per_day = 10;
		int pick_date_deviation = 3;
		DatabaseObject order_list = Generator.orderNormalDatebound(avg_order_per_day, 3, start_date, end_date, pick_date_deviation);
		tlbx.uploadToDatabase(order_list, "orders");
		ArrayList<Object> sku_id_list = new ArrayList<Object>();
		for (HashMap<String, Object> sku : sku_list) sku_id_list.add( sku.get("id"));
		ArrayList<Object> order_id_list = new ArrayList<Object>();
		for (HashMap<String, Object> order : order_list) order_id_list.add( order.get("id"));
		DatabaseObject item_list = Generator.line_item_fixn(5, 3, sku_id_list, order_id_list);
		tlbx.uploadToDatabase(item_list, "line_item");
		DatabaseObject arc_list, node_list, slot_list;
		arc_list = tlbx.getTableFromDatabase("arc");
		node_list = tlbx.getTableFromDatabase("node");
		slot_list = tlbx.getTableFromDatabase("slot");
		DatabaseObject sku_pick_list = PickSeq.order_in_one_all_from_db(tlbx);
		
	}
}
