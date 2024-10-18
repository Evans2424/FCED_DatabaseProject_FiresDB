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

   
    
    # Close the connection when done
    conn_mgr.close()

if __name__ == "__main__":
    main()
