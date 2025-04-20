import pyodbc
import os
from dotenv import load_dotenv

def test_connection():
    load_dotenv()
    
    # Get connection details
    server = os.getenv('DB_SERVER', 'DESKTOP-GP07DFE')
    database = os.getenv('DB_NAME', 'RetailSalesDB')
    
    print("\nTesting SQL Server Connection...")
    print(f"Server: {server}")
    print(f"Database: {database}")
    
    try:
        # List available drivers
        print("\nAvailable ODBC drivers:")
        drivers = [x for x in pyodbc.drivers() if x.startswith('SQL Server')]
        print(drivers)
        
        if not drivers:
            print("No SQL Server ODBC drivers found!")
            return
            
        # Try to connect
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        print(f"\nAttempting connection with: {conn_str}")
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("\nConnection successful!")
        
        # Test queries
        print("\nTesting queries:")
        
        # Test Customers table
        try:
            cursor.execute("SELECT COUNT(*) FROM Customers")
            count = cursor.fetchone()[0]
            print(f"Found {count} customers")
            
            cursor.execute("SELECT TOP 1 * FROM Customers")
            row = cursor.fetchone()
            if row:
                print("Sample customer:", row)
        except Exception as e:
            print(f"Error querying Customers: {str(e)}")
        
        # Test Products table
        try:
            cursor.execute("SELECT COUNT(*) FROM Products")
            count = cursor.fetchone()[0]
            print(f"Found {count} products")
            
            cursor.execute("SELECT TOP 1 * FROM Products")
            row = cursor.fetchone()
            if row:
                print("Sample product:", row)
        except Exception as e:
            print(f"Error querying Products: {str(e)}")
            
        conn.close()
        
    except Exception as e:
        print(f"Connection failed: {str(e)}")

if __name__ == '__main__':
    test_connection() 