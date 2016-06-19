package warehouslayout;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Date;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

import java.sql.ResultSetMetaData;

public class Toolbox {
	private Connection conn = null;
	private String user, password, host, database;
	public final static int MILISECONDS_IN_DAY = 3600000 * 24; 
	public static void main(String[] args) {
		Statement stmt = null;
		ResultSet rs = null;
		Toolbox tb = new Toolbox();
		Connection conn = tb.connection("root", "", "localhost", "picksystem_nt");
		//tb.run_sql("/home/behnam/warehouselayout/trunk/python/tables.sql");
		
		String[] nodeItems = {"id", "name", "x", "y", "z", "type"};
		Object[] nodeValues = {235, "mardas", 10, 10, 10, "Picker"};
		HashMap<String, Object> node = setHashMap(nodeItems, nodeValues);
		System.out.println(tb.uploadToDatabase(node, "node"));
		tb.getTableFromDatabase("arc");
	}
	
	public Toolbox(String userIn, String passwordIn, String hostIn, String databaseIn) {
		connection(userIn, passwordIn, hostIn, databaseIn);
	}
	
	public Toolbox() {
		return;
	}
	
	public Connection connection(String userIn, String passwordIn, String hostIn, String databaseIn) {
		try {
			Class.forName("com.mysql.jdbc.Driver").newInstance();
		}
		catch (Exception ex) {
			ex.printStackTrace();
		}
		
		try {
			String url = "jdbc:mysql://" + hostIn + "/" + databaseIn;
			if (userIn != null && userIn.length() != 0) {
				url = url + "?user=" + userIn;
				if (passwordIn != null && passwordIn.length() != 0) url = url + "&pasword=" + passwordIn;
			}
			conn = DriverManager.getConnection(url);
			conn.setAutoCommit(false);
			return conn;
		}
		catch (SQLException ex) {
			printException(ex);
			return null;
		}
		finally {
			this.user = userIn;
			this.password = passwordIn;
			this.host = hostIn;
			this.database = databaseIn;
		}
	}
	
	public void run_sql(String path) {
		Statement stmt = null;
		BufferedReader br = null;
		try {
			FileReader fr = new FileReader(path);
			br = new BufferedReader(fr);
			String thisLine = "";
			StringBuilder sb = new StringBuilder();
			stmt = conn.createStatement();
			while ((thisLine = br.readLine()) != null) {
				sb.append("\n");
				sb.append(thisLine);
				if (thisLine.indexOf(";") >= 0) {
					stmt.execute(sb.toString());
					sb = new StringBuilder();
				}
			}
			conn.commit();
		}
		catch (SQLException ex) {
			printException(ex);
		}
		catch(Exception ex) {
			ex.printStackTrace();
		}
		finally {
			if (stmt != null) {
				try {
					stmt.close();
				}
				catch (SQLException ex) {}
			}
			if (br != null) {
				try {
					br.close();
				}
				catch (Exception ex) {}				
			}
		}
	}
	
	public DatabaseObject runQuery(String query) {
		Statement stmt = null;
		ResultSet rs = null;
		DatabaseObject items = null;
		try {
			stmt = this.conn.createStatement();
			rs = stmt.executeQuery(query);
			items = this.resultSetToMap(rs);
		}
		catch (SQLException ex) {
			printException(ex);
		}
		catch(Exception ex) {
			ex.printStackTrace();
		}
		finally {
			if (stmt != null) {
				try {
					stmt.close();
				}
				catch (SQLException ex) {}
			}
			if (rs != null) {
				try {
					rs.close();
				}
				catch (SQLException ex) {}
			}
		}
		return items;
	}
	
	public boolean uploadToDatabase(DatabaseObject items, String table) {
		Statement stmt = null;
		boolean isSuccessful = false;
		try {
			stmt = conn.createStatement();
			System.out.println("Uploading to " + table);
			String query = "delete from " + database + "." + table;
			stmt.execute(query);
			for (HashMap<String, Object> item : items) {
				String keys = "(", values = "(";
				int count = 0;
				for (String key : item.keySet()) {
					if (count++ != 0) {
						keys = keys + ", ";
						values = values + ", ";
					}
					keys += key;
					Object value = item.get(key);
					if (!(value instanceof Integer)) {
						values += "\"" + value + "\"";
					}
					else values += value;
				}
				keys += ")";
				values += ")";
//				System.out.println(keys + "\n" +  values);
				query = "INSERT INTO " + database + "." + table + keys + " values " + values;
				stmt.execute(query);				
			}
			conn.commit();
			isSuccessful = true;
			System.out.println("Uploading successful");
		}
		catch (SQLException ex) {
			printException(ex);
		}
		finally {
			if (stmt != null) {
				try {
					stmt.close();
				}
				catch (SQLException ex) {}
			}
		}
		return isSuccessful;
	}
	
	
	public boolean uploadToDatabase(HashMap<String, Object> items, String table) {
		Statement stmt = null;
		boolean isSuccessful = false;
		try {
			stmt = conn.createStatement();
			System.out.println("Uploading to " + table);
			String query = "delete from " + database + "." + table;
			stmt.execute(query);
			String keys = "(", values = "(";
			int count = 0;
			for (String key : items.keySet()) {
				if (count++ != 0) {
					keys = keys + ", ";
					values = values + ", ";
				}
				keys += key;
				Object value = items.get(key);
				if (value instanceof String) {
					values += "\"" + value + "\"";
				}
				else values += value;
			}
			keys += ")";
			values += ")";
//			System.out.println(keys + "\n" +  values);
			query = "INSERT INTO " + database + "." + table + keys + " values " + values;
			stmt.execute(query);				
			conn.commit();
			isSuccessful = true;
			System.out.println("Uploading successful");
		}
		catch (SQLException ex) {
			printException(ex);
		}
		finally {
			if (stmt != null) {
				try {
					stmt.close();
				}
				catch (SQLException ex) {}
			}
		}
		return isSuccessful;
	}
	
	public DatabaseObject getTableFromDatabase(String tableName) {
		System.out.println("Reading from " + tableName);
		Statement stmt = null;
		ResultSet rs = null;
		try {
			DatabaseObject items = new  DatabaseObject(); 
			stmt = this.conn.createStatement();
			String query = "select * from " + tableName;
			rs = stmt.executeQuery(query);
			items = this.resultSetToMap(rs);
			System.out.println("Read successful!");
			return items;
		}
		catch (SQLException ex) {
			printException(ex);
		}
		finally {
			if (stmt != null) {
				try {
					stmt.close();
				}
				catch (Exception ex) {}
			}
			if (rs != null) {
				try {
					rs.close();
				}
				catch (Exception ex) {}
			}
		}
		return null;
	}
	
	public DatabaseObject resultSetToMap(ResultSet rs) {
		try {
			DatabaseObject items = new  DatabaseObject();
			ResultSetMetaData rsmd = rs.getMetaData();
			int columnNumber = rsmd.getColumnCount();
			String labels[] = new String[columnNumber];
			for (int i = 1; i <= labels.length; i++) {
//			note that column numbering in rsmd starts at 1
				labels[i - 1] = rsmd.getColumnName(i);
			}
//		System.out.println(Arrays.toString(labels));
			while (rs.next()) {
				Object row[] = new Object[columnNumber];
				for (int i = 0; i < columnNumber; i++) {
					row[i] = rs.getObject(i + 1);
				}
//			System.out.println(Arrays.toString(row));
				items.add(setHashMap(labels, row));
			}
			return items;
		}
		catch (SQLException ex) {
			printException(ex);
			return null;
		}
	}
	public static <T, V> HashMap<T, V> setHashMap(T[] keySet, V[] valueSet) {
		if (keySet.length != valueSet.length) return null;
		HashMap<T, V> items = new HashMap<T, V>();
		for (int i = 0; i < keySet.length; i++) {
			items.put(keySet[i], valueSet[i]);
		}
		return items;
	}
	
	public static <T, V> void add(ArrayList<HashMap<T, V>> items, T[] keySet, V[] valueSet) {
		items.add(setHashMap(keySet, valueSet));
	}
	
	public static int daysBetween(Date d1, Date d2) {
		long ms1 = d1.getTime();
		long  ms2 = d2.getTime();
		if (ms2 < ms2) return -1;
		return (int) (ms2 - ms1) / (3600000 * 24);
	}
	
	public static double getGaussian(double aMean, double aVariance){
	    return aMean + (new Random(System.currentTimeMillis())).nextGaussian() * aVariance;
	  }

	private static void printException(SQLException ex) {
		System.out.println("SQLException: " + ex.getMessage());
		System.out.println("SQLState: " + ex.getSQLState());
		System.out.println("VendorError: " + ex.getErrorCode());
	}
}
