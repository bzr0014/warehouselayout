package warehouslayout;

import java.util.ArrayList;
import java.util.HashMap;

public class PickSeq {
	public static DatabaseObject order_in_one_all_from_db(Toolbox tb) {
//		try one query and looping once
		String query = "select orders.id, sku_id from line_item, orders"
				+ "where line_item.order_id = orders.id"
				+ "order by orders.id ASC";
		 return tb.runQuery(query);
	}
}
