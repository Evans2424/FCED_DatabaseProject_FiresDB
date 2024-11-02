import psycopg
#from tkinter import messagebox
from tabulate import tabulate
import pandas as pd
from datetime import datetime
import uuid

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
    def export_to_csv(self,dataframe):
        random_uuid = uuid.uuid4()
        now = datetime.now()
        # Format the datetime, removing the decimal point from seconds
        formatted_time = now.strftime("%Y-%m-%d")
        dataframe.to_csv(f"EXPORT_{formatted_time}_{random_uuid}.csv", index=False)
        print("Export Done")


       
    
