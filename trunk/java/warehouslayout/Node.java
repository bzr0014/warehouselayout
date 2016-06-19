package warehouslayout;

import java.util.ArrayList;


public class Node {
	
	int id;
	enum Color { WHITE, GRAY, BLACK };
	ArrayList<Node>  adj;  // linked list of pointers to adjacent nodes 
	Color color;
	int d;  // distance from root in BFS, discovery time in DFS
	int f;  // finish time in DFS
	Node pi; // parent in DFS or BFS tree
	
	public String toString() {
		return id + "";
	}
}
