package warehouslayout;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class Locap {
	public static DatabaseObject random(ArrayList<Object> slot_list, ArrayList<Object> sku_id_list) {
		DatabaseObject slot_sku_list = new DatabaseObject();
		Collections.shuffle(sku_id_list);
		int size = Math.min(slot_list.size(), sku_id_list.size());
		HashMap<String, Object> slot_sku = new HashMap<String, Object>();
		for (int i = 0; i < size; i++) {
			slot_sku.put("slot_sku_id", sku_id_list.get(i));
			slot_sku.put("quantity", 5);
			slot_sku_list.add(slot_sku);
		}
		return slot_sku_list;
	}
}
