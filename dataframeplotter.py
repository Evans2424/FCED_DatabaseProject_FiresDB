import os
import uuid
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class query_plotter:
    def __init__(self):
        self.height = 10
        self.width = 8
        self.title = ""

    def setfigize(self, height, width):
        self.height = height
        self.width = width

    def setplottitle(self, title):
        self.title = title

    def bar_plot(self, df, x, y):
        plt.figure(figsize=(self.height, self.width))
        plt.title(self.title)
        plt.xticks(rotation=90)
        sns.barplot(df, x=x, y=y)
        
        # Ensure the Output directory exists
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct the file path
        random_uuid = uuid.uuid4()
        file_path = os.path.join(output_dir, f"BarPlot_{random_uuid}.pdf")
        
        plt.savefig(file_path)
        print(f"Bar Plot Saved to {file_path}")

    def line_plot(self, df, x, y):
        plt.figure(figsize=(self.height, self.width))
        plt.title(self.title)
        plt.xticks(rotation=90)
        sns.lineplot(df, x=x, y=y)
        
        # Ensure the Output directory exists
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct the file path
        random_uuid = uuid.uuid4()
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d")
        file_path = os.path.join(output_dir, f"Plot_{formatted_time}_{random_uuid}.pdf")
        
        plt.savefig(file_path)
        print(f"Plot Saved to {file_path}")
        

    