package warehouslayout;

import java.util.ArrayList;



public class Graph { 
    // Nodes are numbered 1,2,...,numNodes;
    // There IS a node zero, but it is never used
    // The .size() function on nodeList and edgeList DOES NOT return the number of nodes or edges
    // use numNodes and numEdges instead
   public ArrayList<Node> nodeList;
   public ArrayList<Edge> edgeList; 
   public int numNodes = 0;
   public int numEdges = 0;
   private static int latestNodeId = 1;

   public Graph() { 
      nodeList = new ArrayList<Node>();
      edgeList = new ArrayList<Edge>();
      Node n = new Node();
      nodeList.add(n);
      Edge e = new Edge();
      edgeList.add(e);
   } 


   public Node addNode() { 
      Node n = new Node();
      n.id = latestNodeId++;
      nodeList.add(n);
      numNodes++;
      n.adj = new ArrayList<Node>(); 
      System.out.println("nodeList.size="+nodeList.size());
      return n;
   }

   public Edge addEdge(Node u, Node v) {
      u.adj.add(v);
      Edge e = new Edge();
      e.head = u; 
      e.tail = v;
      numEdges++;
      edgeList.add(e);
      return e;
   } 
}
