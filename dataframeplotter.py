import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import uuid

class query_plotter:
    def __init__(self):
        self.height = 10
        self.width = 10
        self.title = ''
    def setfigize(self,height1,width1):
        self.height = height1
        self.width = width1
    def setplottitle(self,titlestr=''):
        self.title = titlestr
    def bar_plot(df,x,y): 
        return None
        #TBD  

    def line_plot(self,df,x,y):
        plt.figure(figsize = (self.height,self.width))
        plt.title(self.title)
        plt.xticks(rotation=90) 
        sns.lineplot(df,x=x,y=y)
        random_uuid = uuid.uuid4()
        now = datetime.now()
        # Format the datetime, removing the decimal point from seconds
        formatted_time = now.strftime("%Y-%m-%d")
        plt.savefig(f"Plot_{formatted_time}_{random_uuid}.pdf")
        print("Plot Saved")
        

    