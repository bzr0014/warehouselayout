package warehouslayout;

import java.sql.Date;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Random;

public class Generator {
	public static DatabaseObject sku(int sku_count) {
		DatabaseObject skus = new DatabaseObject();
		for (int i = 0; i < sku_count; i++) {
			HashMap<String, Object> sku = new HashMap<String, Object>();
			sku.put("id", i + 1);
			sku.put("name", "sku" + (i+1));
			sku.put("description", "");
			sku.put("class", "A");
			skus.add(sku);
		}
		return skus;
	}
	public static DatabaseObject orderNormalDatebound(double avgOrderPerDay, double stdev, Date startDate, Date endDate, int pickDateDeviation) {
		DatabaseObject orders = new DatabaseObject();
		long startDayInMiliseconds = startDate.getTime();
		int numDays = Toolbox.daysBetween(startDate, endDate);
		int orderNum = 1;
		for (int i = 0; i < numDays; i++) {
			int today_order_count = (int) Math.max(Toolbox.getGaussian(avgOrderPerDay, stdev), 0);
			for (int j = 0; j < today_order_count; j++) {
				orderNum++;
				Date orderDate = new Date(startDayInMiliseconds + j * Toolbox.MILISECONDS_IN_DAY);
				Date pickDate = new Date( startDayInMiliseconds + (j + pickDateDeviation) * Toolbox.MILISECONDS_IN_DAY );
				String orderCustomer = "Customer " + orderNum;
				
				HashMap<String, Object> orderItem = new HashMap<String, Object>();
				orderItem.put("id", orderNum);
				orderItem.put("order_dtg", orderDate);
				orderItem.put("target_pick_dtg", pickDate);
				orderItem.put("customer", orderCustomer);
				orderItem.put("order_number", orderNum);
				orders.add(orderItem);
			}
		}
		return orders;
	}
	
	public static ArrayList<Object> orderDatebound(double orderPerDay, Date startDate, Date endDate, int pickDateDeviation) {
		ArrayList<Object> orders = new ArrayList<Object>();
		long startDayInMiliseconds = startDate.getTime();
		int numDays = Toolbox.daysBetween(startDate, endDate);
		int orderNum = 1;
		for (int i = 0; i < numDays; i++) {
			for (int j = 0; j < orderPerDay; j++) {
				int order_number = j + 1;
				Date orderDate = new Date(startDayInMiliseconds + j * Toolbox.MILISECONDS_IN_DAY);
				Date pickDate = new Date( startDayInMiliseconds + (j + pickDateDeviation) * Toolbox.MILISECONDS_IN_DAY );
				String orderCustomer = "Customer " + orderNum;
				
				ArrayList<Object> orderItem = new ArrayList<Object>();
				orderItem.add(order_number);
				orderItem.add(orderDate);
				orderItem.add(pickDate);
				orderItem.add(orderCustomer);
				orders.add(orderItem);
			}
		}
		return orders;
	}
	
public static DatabaseObject line_item_fixn (int linePerOrder, int quantity, ArrayList<Object> skuIdList, ArrayList<Object> orderIdList) {
	DatabaseObject order_skus = new DatabaseObject();
	Collections.shuffle(skuIdList);
	for (int i = 0; i < orderIdList.size(); i++) {
			for (int j = 0; j < linePerOrder; j++) {
				HashMap<String, Object> order_sku = new HashMap<String, Object>();
				order_sku.put("quantity", quantity);
				order_sku.put("order_id", orderIdList.get(i));
				order_sku.put("sku_id", skuIdList.get(j));
				order_skus.add(order_sku);
			}
		}
	return order_skus;
	}
}
