import psycopg
#from tkinter import messagebox
from tabulate import tabulate
import pandas as pd
from datetime import datetime
import uuid
import os

class DatabaseManager:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager

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
    
    def export_to_csv(self, dataframe):
        random_uuid = uuid.uuid4()
        now = datetime.now()
        # Format the datetime, removing the decimal point from seconds
        formatted_time = now.strftime("%Y-%m-%d")
        
        # Ensure the Output directory exists
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct the file path
        file_path = os.path.join(output_dir, f"EXPORT_{formatted_time}_{random_uuid}.csv")
        
        # Export the dataframe to the CSV file
        dataframe.to_csv(file_path, index=False)
        print("Export Done")


       
    
