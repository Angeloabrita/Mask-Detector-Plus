import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def pushData(value):

    now = datetime.now() 
    timeNow = now.strftime("%d/%m/%Y, %H:%M:%S")

    with open("data.json", "r+") as file:
        data = json.load(file)
        a = {value: 1, "date": timeNow}
        data["data"].append(a)
        file.seek(0)
        json.dump(data, file)

def erase_data():
   now = datetime.now()  
   timeNow = now.strftime("%d/%m/%Y, %H:%M:%S")

   with open('data.json', 'r+') as data_file:
    data = json.load(data_file)
    data.clear()
    

    with open('data.json', 'w') as data_file:
        a = {"data":[{"NoMask": 0, "date": timeNow },{"WithMask": 0, "date": timeNow }]}
        data = json.dump(a, data_file)
            
    
        

def plot_data():

    '''read json file data.json group with and without mask by date and plot it'''

    with open("data.json", "r+") as file:
        data = json.load(file)
        table = pd.DataFrame(data['data']) 
        table['WithMask'].fillna(0, inplace=True)
        table['NoMask'].fillna(0, inplace=True)      
        table['date']= pd.to_datetime(table['date'])
        table= table.groupby([table['date'].dt.strftime('%m/%d/%Y')]).sum().reset_index()
       
        #do plot by date
        labels=table['date']
        x = np.arange(len(labels))  # the label locations
        width = 0.2 # the width of the bars
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Mask detector plot at %s' % datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

        print(table['WithMask'],table['NoMask'])

        rects1 = ax.bar(x - width/2, table['WithMask'], width,color='#02bf61',label='With Mask')
        rects2 = ax.bar(x + width/2, table['NoMask'], width, color= '#b00000', label='Without Mask')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Total')
        ax.set_title('Total by date')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        #Attach a text label above each bar in *rects*, displaying its height. 
        def autolabel(rects):   
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()

        plt.show()
      
     
        
def export_data():
    '''convert and explort data.json at Documents file'''
    home = os.path.expanduser('~')
    folder_path = os.path.join(home,'Documents')
    check = os.path.isdir(folder_path)

    if check:
        try:
            with open("data.json", "r+") as file:
                data = json.load(file)
                table = pd.DataFrame(data['data'])
                table['WithMask'].fillna(0, inplace=True)
                table['NoMask'].fillna(0, inplace=True)
                table['date']= pd.to_datetime(table['date'])
                  
                 
                table.to_excel(folder_path + "\mask-detector.xlsx", index=False)
        except OSError:
            print("erroexeption")       
    else:
        print("erroelse")


        
