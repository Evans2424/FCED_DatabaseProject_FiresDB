from ConnectionManager import ConnectionManager  
from GUI import Menu
from DatabaseManager import DatabaseManager

CSV_FILE = 'Data/Registos_Incendios_SGIF_2021_2023.csv'


DB_PARAMS = {
    'database': 'up202108818',
    'user': 'up202108818',
    'password': 'up202108818',
    'host': 'dbm.fe.up.pt',
    'port': '5433'
}


def main():

    # Instantiate the ConnectionManager class
    conn_mgr = ConnectionManager(**DB_PARAMS)
    db_mgr = DatabaseManager(conn_mgr)

        # Attempt to establish connection to PostgreSQL
    if conn_mgr.connect():
        # Proceed only if connection is successful
        main = Menu(db_mgr)
        main.main_menu()
    else:
        print("Failed to establish a connection. Exiting program.")


    # Close the connection when done
    conn_mgr.close()

if __name__ == "__main__":
    main()