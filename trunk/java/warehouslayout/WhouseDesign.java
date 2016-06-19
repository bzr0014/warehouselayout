package warehouslayout;

import java.util.ArrayList;
import java.util.HashMap;

public class WhouseDesign {
	public static void twoByOne(int width, int length, int node_distance,
			int center_aisle_width, int bottom_aisle_width, int aisle_width,
			int aisle_angle_degree, int slots_per_node) {
		
		String nodeTags[] = {"id", "name", "x", "y", "z", "type"};
		String arcTags[] = {"id", "travel_factor", "head_node_id", "tail_node_id"};
		String slotTags[] = { "id", "node_id", "sku_id", "quantiti" };
		
		Object depot_node[] = {1,"N0",0,0,0,"picker"};
		Object bottom_center_node[] = {2,"N1",depot_node[3],bottom_aisle_width/2.0,0,"picker"};
		Object bottom_top_node[] = {3,"N2",depot_node[3],bottom_aisle_width,0,"picker"};
		
		DatabaseObject nodes = new DatabaseObject();
		Toolbox.add(nodes,nodeTags, depot_node);
		Toolbox.add(nodes,nodeTags, bottom_center_node);
		Toolbox.add(nodes,nodeTags, bottom_top_node);
		
		
		DatabaseObject arcs = new DatabaseObject();
	    // Creates the first to arc (from depot to the main node and from the bottom main node to top main node
	    {
	    	Object arc[] = {arcs.size()+1,1,depot_node[0],bottom_center_node[0]};
	    	Toolbox.add(arcs, arcTags, arc);
	    }
	    {
	    	Object arc[] = { arcs.size() + 1, 1, bottom_center_node[0], bottom_top_node[0] };
	    	Toolbox.add(arcs, arcTags, arc);
	    }
	    //checks if the angle is 90 or 0
	    double aisle_angle_pi = aisle_angle_degree / 180.0 * Math.PI;
	    double angle_factor_x = 0;
	    double angle_factor_y = 0;
	    if (aisle_angle_degree == 0) angle_factor_x = 0;
	    else if (aisle_angle_degree == 90) angle_factor_y = 0;
	    else if (aisle_angle_degree<90 && aisle_angle_degree>0) {
	    	angle_factor_y = 1 / Math.cos(aisle_angle_pi);
	    	angle_factor_x = 1 / Math.sin(aisle_angle_pi);	    	
	    }
	    
	    if (aisle_angle_degree < 90 && aisle_angle_degree > 0) {
	    	double x_distance = node_distance * angle_factor_x;
	    	double y_distance = node_distance * angle_factor_y;
	    	int section_size[] = {
	    			(length - width) / 2,
	    			width - bottom_aisle_width };
	    	for (int i = 0; i < section_size[0] / x_distance + 1; i++) {
	    		if (i == 1) {
	    			
	    		}
	    	}
	    }
	    
	}

}
