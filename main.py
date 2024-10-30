
from ConnectionManager import ConnectionManager  
from load_fires import delete_all_data, insert_data


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

    # Establish connection to PostgreSQL
    conn_mgr.connect()

    cursor = conn_mgr.connection.cursor()

    delete_all_data(conn_mgr.connection)
    insert_data(conn_mgr.connection, CSV_FILE)


    
    # Close the connection when done
    conn_mgr.close()

if __name__ == "__main__":
    #main()
    print("Teste")