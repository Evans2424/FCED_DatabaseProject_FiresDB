
import psycopg



class ConnectionManager:
    def __init__(self, database, user, password, host="localhost", port="5432"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                options='-c search_path=schema'
            )
            print("Connected to the PostgreSQL database successfully")
        except psycopg.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
