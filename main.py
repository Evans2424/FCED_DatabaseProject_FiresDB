from ConnectionManager import ConnectionManager  

def main():
    database = "up202108818"
    user = "up202108818"
    password = "up202108818"
    host = "dbm.fe.up.pt"
    port = "5433"     

    # Instantiate the ConnectionManager class
    conn_mgr = ConnectionManager(database, user, password, host, port)

    # Establish connection to PostgreSQL
    conn_mgr.connect()

    cursor = conn_mgr.connection.cursor()
    
    # Define the SQL query
    query = "SELECT * FROM airport;"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Print each row
    for row in rows:
        print(row)

    
    # Close the connection when done
    conn_mgr.close()

if __name__ == "__main__":
    main()
