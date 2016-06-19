package warehouslayout;

import java.util.Scanner;

import warehouslayout.Node.Color;

import java.util.ArrayList;
import java.util.LinkedList;
import java.io.File;
import java.io.FileNotFoundException;

public class prog2_bzr0014 { 
	int MAX_VALUE = 2^30; 
	int WHITE = 1; 
	int GRAY = 2; 
	int BLACK = 3; 
//	Scanner scanner = new Scanner(System.in);
	static Scanner scanner = null;
	Graph G = new Graph(); 

	public static void main(String args[]) throws FileNotFoundException { 
		//Scanner scanner = new Scanner(new File(args[0]));
	  scanner =  new Scanner(new File("/home/behnam/Desktop/COMP3270-Algorithms/Program II/testfile1.input"));
		new prog2_bzr0014().run();
	} 

	public void BFS(Graph G, Node s) {
	// implement BFS here
		for (Node u: G.nodeList) {
			u.color = Color.WHITE;
			u.d = MAX_VALUE;
			u.pi = null;
		}
		s.color = Color.GRAY;
		s.d = 0;
		s.pi = null;
		LinkedList<Node> q = new LinkedList<Node>();
		q.add(s);
		while (!q.isEmpty()) {
			Node u = q.remove();
			for (Node v : u.adj) {
				if (v.color == Color.WHITE) {
					v.color = Color.GRAY;
					v.d = u.d + 1;
					v.pi = u;
					q.add(v);
				}
				u.color = Color.BLACK;
			}
		}
	} 

	public void printBFSTree(Graph G) {
		for (Node n: G.nodeList) { 
			if (G.nodeList.indexOf(n) != 0) { 
				System.out.println("Node:"+G.nodeList.indexOf(n)+", parent="+G.nodeList.indexOf(n.pi)+", depth="+n.d);
			}
		}
	} 
	
	public ArrayList<Node> shortestSubtour(Graph G, Node s) {
		ArrayList<Node> path = new ArrayList<Node>();
		for (Node u: G.nodeList) {
			u.color = Color.WHITE;
			u.d = MAX_VALUE;
			u.pi = null;
		}
		s.color = Color.GRAY;
		s.d = 0;
		s.pi = null;
		LinkedList<Node> q = new LinkedList<Node>();
		q.add(s);
		while (!q.isEmpty()) {
			Node u = q.remove();
			for (Node v : u.adj) {
				System.out.println("checking: " + u + ", " + v);
				if (v.color == Color.WHITE) {
					v.color = Color.GRAY;
					v.d = u.d + 1;
					v.pi = u;
					q.add(v);
					}
				else if (v == s) {
					path.add(u);
					q = new LinkedList<Node>();
					break;
					}
				u.color = Color.BLACK;
				}
			}
		if (path.isEmpty()) return null;
		Node n = path.get(0);
		while (n.pi != null) {
			System.out.print(n + ", ");
			path.add(n.pi);
			n = n.pi;
		}
		//path.add(n);
		System.out.print(n);
		System.out.println();
		return path;
		}
	
	public ArrayList<Node> shortestTotalSubtour(Graph G) {
		ArrayList<Node> shortestPath = new ArrayList<Node>();
		int shortestPathLength = G.numEdges + 1;
		int count = 0;
		for (Node u : G.nodeList) {
			if (count++ == 0) continue;
			ArrayList<Node> path = shortestSubtour(G, u);
			if (shortestPathLength > path.size()) {
				shortestPathLength = path.size();
				shortestPath = path;
			}
		}
		System.out.println("Printing shortest path: ");
		count = 0;
		for (Node n : shortestPath) {
			if (count++ != 0) System.out.print(", ");
			System.out.print(n.id);
		}
		System.out.println();
		return shortestPath;
	}

	 // used in DFS 
	int time; 

	public void DFS(Graph G) { 
	// implement DFS here
		for (Node u : G.nodeList) {
			u.color = Color.WHITE;
			u.pi = null;
		}
		time = 0;
		for (Node u : G.nodeList) {
			if (G.nodeList.indexOf(u) != 0) {
				if (u.color == Color.WHITE) 
					DFS_VISIT(G, u);
			}
		}
	}

	public void DFS_VISIT(Graph G, Node u) { 
	// implement DFS_VISIT here 
		time = time + 1;
		u.d = time;
		u.color = Color.GRAY;
		for (Node v : u.adj) {
			if (v.color == Color.WHITE) {
				v.pi = u;
				DFS_VISIT(G, v);
			}
		}
		u.color = Color.BLACK;
		time = time + 1;
		u.f = time;
	} 

	public void printDFSForest(Graph G) {
		for (Node n: G.nodeList) { 
			if (G.nodeList.indexOf(n) != 0) { 
				System.out.println("Node:"+G.nodeList.indexOf(n)+", parent="+G.nodeList.indexOf(n.pi)+", d=="+n.d+", f="+n.f);
			}
		}
	} 

	public void run() {
	// process input, first line is number of nodes, followed by number of edges, each less than 500
	// then each line has one edge, with tail first, then head
		int numNodes = scanner.nextInt();
		int numEdges = scanner.nextInt();
	//System.out.println("numNodes="+numNodes+" numEdges="+numEdges);
	// create the legit nodes
		for(int j = 1; j <=  numNodes ; j++) { 
		 //System.out.println("added node "+j);
			Node n = G.addNode();
		} 
	
	// process the legit edges; 
		for (int j = 1; j <= numEdges; j++) {
			int headNum = scanner.nextInt();
			int tailNum = scanner.nextInt();
		 //System.out.println("added edge head="+headNum+" tail="+tailNum);
			Node head = G.nodeList.get(headNum);
			Node tail = G.nodeList.get(tailNum);
			G.addEdge(head,tail); 
		}	  
	
	//  print out the graph to verify it is correctly read, using the adj list
		for (Node n: G.nodeList) { 
				// have to handle the null zero node 
			if (G.nodeList.indexOf(n) != 0) {  
				System.out.print("node "+G.nodeList.indexOf(n)+":");
				for (Node v: n.adj) { 
					System.out.print(G.nodeList.indexOf(v)+" ");
				} 
				System.out.println();
			}
		} 
	
	// do a BFS from node 1 
		BFS(G,G.nodeList.get(1)); 
	
	// print the result of the BFS
		printBFSTree(G); 
	
	// do a DFS 
		DFS(G); 
	
	//print the result of the DFS
		printDFSForest(G);
		
		shortestTotalSubtour(G);
	}

}
