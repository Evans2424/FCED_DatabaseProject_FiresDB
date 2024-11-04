
import psycopg



class ConnectionManager:
    def __init__(self, database, user, password, host="localhost", port="5432"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.is_connected = False  # New attribute to track connection status


    def connect(self):
        try:
            # Attempt to establish a connection
            self.connection = psycopg.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                options='-c search_path=public'
            )
            self.is_connected = True
            print("Connected to the PostgreSQL database successfully")
            return True  # Return True to indicate a successful connection
        except psycopg.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            self.is_connected = False
            return False  # Return False if connection fails

    def close(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
            print("Connection closed")

