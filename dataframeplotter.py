import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

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
        self.setfigize(self.height,self.width)
        sns.barplot(df,x=x,y=y)   

    def line_plot(self,df,x,y):
        plt.figure(figsize = (self.height,self.width))
        plt.title(self.title)
        plt.xticks(rotation=90) 
        sns.lineplot(df,x=x,y=y)
        plt.savefig(f"Plot_{datetime.now()}.pdf")
        print("Plot Saved")
        

    