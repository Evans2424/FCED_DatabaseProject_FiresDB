import psycopg
from tkinter import messagebox
from tabulate import tabulate

class DatabaseManager:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

    def fires_from_Porto(self):
        cursor = self.connection_manager.connection.cursor()
        cursor.execute("""
            SELECT fi.*
            FROM fireincidents fi
            JOIN location_info li ON fi.location_id = li.id
            JOIN parishes p ON li.parish_id = p.id
            JOIN municipality m ON p.municipality_id = m.id
            JOIN district d ON m.district_id = d.id
            WHERE d.districtname = 'Porto'
        """)
        records = cursor.fetchall()
        cursor.close()
        return records
    
    def display_records(self, records):
        if records:
            # Define headers for table
            headers = ["ID", "Incident Date", "Severity", "Location ID"]  # Customize these headers
            # Print records in a tabular format
            print(tabulate(records, headers=headers, tablefmt="grid"))
        else:
            print("No records found.")

       
    
