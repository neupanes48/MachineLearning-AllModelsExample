# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:12:59 2017

@author: Suraj Neupane
"""

import pandas as pd;
import numpy as np;
import scipy as sp;


#from lxml import html
#import request
from urllib.request import urlopen
#import datetime as dt
import matplotlib.pyplot as plt
#%matplotlib inline

#get market data 
def get_google_data(symbol, period, days):
    url_root = 'http://www.google.com/finance/getprices?i='
    url_root += str(period) + '&p=' + str(days)
    url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
    
    #page = requests.get(url_root)
    #data = html.fromstring(page.content)
    print(url_root);
    response = urlopen(url_root)
    readResponse = response.read().decode()
    data = readResponse.split('\n')
    #d = data.split('\n')
    #print(d)
    
    #actual data starts at index = 7
    #first line contains full timestamp,
    #every other line is offset of period from timestamp
    parsed_data = []
    #anchor_stamp = ''
    end = len(data)
    for i in range(7, end):
        cdata = data[i].split(',')
        #if 'a' in cdata[0]:
            #first one record anchor timestamp
            #anchor_stamp = cdata[0].replace('a', '')
            #cts = int(anchor_stamp)
        #else:
        try:
            #coffset = int(cdata[0])
            #cts = int(anchor_stamp) + (coffset * period)
            parsed_data.append((float(cdata[0]), float(cdata[1]), float(cdata[2]), float(cdata[3]), float(cdata[4]), float(cdata[5])))
        except:
            pass # for time zone offsets thrown into data
    
    df = pd.DataFrame(parsed_data)
    
    df.columns = ['ts', 'o', 'h', 'l', 'c', 'v']
    df.as_matrix
    #df.index = df.ts
    
    #del df['ts']
    
    return df
    


#getting data frm google.  Format: Currency or Stock Name, Time Period, and Numbers of days    
eurusd = get_google_data('EURUSD', 3600, 10)

# Setting of plotting datas (optional)

plt.title('Data To analysis');
plt.ylabel('Price');
plt.xlabel('Hours');





#calculating error.
def error(f, x, y):
    return sp.sum((f(x)-y)**2)

#plotting data (command)

#plt.plot(eurusd['h'],'g.',eurusd['o'],'k.',eurusd['l'],'r.'); #plotting high, open and low
#plt.plot(eurusd['o'],'b.');

#Scatter the data two variables.
x = eurusd['ts'];  #display in x-Axis
y = eurusd['o'];   #Display in y-Axis 

plt.scatter(x, y , s=2)
plt.autoscale(tight=True)   
plt.grid(True, linestyle='-', color='0.75')

#Polyfit degree 1
pf1 = np.polyfit(x, y, 1)


# Converting polyfit into equiation y = mx+c
f1 = np.poly1d(pf1)

#making the datas to pass on equiation
fx = np.linspace(0,y.size, 1000)

#f1(fx) passing fx into f1 equiation.
plt.plot(fx , f1(fx), linewidth=1)

print("Error 1:  %s" % error(f1, x, y))


#Same test on 2 degreee polyfit
pf2 = np.polyfit(x, y, 5)
f2 = np.poly1d(pf2)

plt.plot(fx , f2(fx), linewidth=1)

print("Error 2:  %s" % error(f2, x, y))

#Same test on 3 degreee polyfit
pf3 = np.polyfit(x, y, 10)
f3 = np.poly1d(pf3)

plt.plot(fx , f3(fx), linewidth=1)
print("Error 3:  %s" % error(f3, x, y))




#Same test on 3 degreee polyfit
pf4 = np.polyfit(x, y, 100)
f4 = np.poly1d(pf4)

plt.plot(fx , f4(fx), linewidth=1)
print("Error 4:  %s" % error(f4, x, y))



plt.legend(["d=%i" % f1.order], loc="upper left")







#Drawing the stright line.
#fp1, residuals, rank, sv, rcond = sp.polyfit(y, x, y.size, full=True)

#plt.plot(sp.polyfit(x , y, 60),'r--');


#f1 = sp.poly1d(fp1)

#fx = sp.linspace(0,x[-1], 1000) # generate X-values for plotting
#plt.plot(fx, f1(fx), linewidth=4)
#plt.legend(["d=%i" % f1.order], loc="upper left")








plt.show();

#Extra Plot Fitures. 

#plt.ylim(1.06,1.075); # Provides the range of ploting


# red dashes, blue squares and green triangles
#plt.plt(eurusd['o'], 'r--', eurusd['h'], 'bs', eurusd['l'], 'g^')




