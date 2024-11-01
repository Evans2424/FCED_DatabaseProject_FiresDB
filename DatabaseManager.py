import psycopg
#from tkinter import messagebox
from tabulate import tabulate
import pandas as pd
from datetime import datetime

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
    
    def run_select(self,query):
        cursor = self.connection_manager.connection.cursor()
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        records = cursor.fetchall()
        cursor.close()
        return records,column_names

    def show_in_pandas(self,returnofquery):
        response,column =  returnofquery[0],returnofquery[1]   
        df = pd.DataFrame(response,columns = column)
        return df
    def export_to_csv(self,dataframe):
        dataframe.to_csv(f"EXPORT_{datetime.now()}.csv", index=False)

    def display_records(self, records):
        if records:
            # Define headers for table
            headers = ["ID", "Incident Date", "Severity", "Location ID"]  # Customize these headers
            # Print records in a tabular format
            print(tabulate(records, headers=headers, tablefmt="grid"))
        else:
            print("No records found.")

       
    
