#from lxml import html
#import request
from urllib.request import urlopen
import datetime as dt
import pandas as pd

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
    anchor_stamp = ''
    end = len(data)
    for i in range(7, end):
        cdata = data[i].split(',')
        if 'a' in cdata[0]:
            #first one record anchor timestamp
            anchor_stamp = cdata[0].replace('a', '')
            cts = int(anchor_stamp)
        else:
            try:
                coffset = int(cdata[0])
                cts = int(anchor_stamp) + (coffset * period)
                parsed_data.append((dt.datetime.fromtimestamp(float(cts)), float(cdata[1]), float(cdata[2]), float(cdata[3]), float(cdata[4]), float(cdata[5])))
            except:
                pass # for time zone offsets thrown into data
    df = pd.DataFrame(parsed_data)
    df.columns = ['ts', 'o', 'h', 'l', 'c', 'v']
    df.index = df.ts
    del df['ts']
    return df
    


#getting data frm google.  Format: Currency or Stock Name, Time Period, and Numbers of days    
eurusd = get_google_data('EURUSD', 3600, 2)


print(eurusd['o']);
