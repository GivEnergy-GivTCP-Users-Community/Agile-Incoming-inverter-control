#!/usr/bin/Get_Agile_incomming v2 fix applied value stuck at var 10

# importing the requests library
import requests
import json
from datetime import datetime, timedelta
  
# api-endpoint
BASE_URL = "https://api.octopus.energy"
PRODUCT_CODE = "AGILE-FLEX-22-11-25"
TARIFF_CODE = "E-1R-" + PRODUCT_CODE + "-B" # change  the "-B" bit to match your region code
TARIFF_URL = BASE_URL + "/v1/products/" + PRODUCT_CODE + "/electricity-tariffs/" + TARIFF_CODE
  
#setting the time
now = datetime.now()+ timedelta(days = 0)
DATEFROM = now.strftime("%Y-%m-%d")+ "T00:00Z"
newdate = now + timedelta(days = 1)
DATETO = newdate.strftime("%Y-%m-%d")+ "T00:00Z"


# parameter items given here
APIKEY = "your octopus api key"
ACCOUNT = ""
PERIOD_FROM = DATEFROM
PERIOD_TO = DATETO

# defining the outgoing url
URL = TARIFF_URL + "/standard-unit-rates/?" + "period_from=" + PERIOD_FROM + "&period_to=" + PERIOD_TO

#print(URL)
  
# sending Post request and saving the response as inspire key
r = requests.get(URL, auth=(APIKEY,''))

# need to add error check R = 200 go r= <> 200 stop


if r.status_code == 200:

    data = sorted(r.json()['results'], key=lambda k: k['value_inc_vat'])
    tariff_good = '{"results":[ '
    y = 0
    rates = []
    
    for value in data:
         rates.append(value['value_inc_vat'])
        
    MinRate = min(rates)
    MaxRate = max(rates)
    MeanRate = sum(rates)/len(rates)

    
# parse the json list and extract the rates that meet the criteria
    for item in data:
         y = y + 1
         cost = str(item['value_inc_vat'])
         if y < 11:
            #Start_date = str(datetime.fromisoformat(item['valid_from'][:-1]))
            tariff_good += '{ "from": '+ '"' + item['valid_from'] + '",' + '"Cost": '+ '"' + cost + '"},'

            
# remove the added , 
    CheapRate = tariff_good[:-1] + ' ]}'
    
# create a new json object and order it by date time
    json_object = json.loads(CheapRate)
    json_object['results'].sort(key=lambda x: x['from'], reverse=False)
    data = json_object['results']
    
# create final json output
    tariff_new = '{'
    y = 0
    for item in data:
         y = y + 1
         run_num = 'Run_number' +str(y)
         cost_num = 'cost_number' +str(y)
         start_num = 'start_time' +str(y)
         end_num = 'end_time' +str(y)
         min_rate = 'min_rate' + str(y)
         max_rate = 'max_rate' + str(y)
         mean_rate = 'mean_rate' + str(y)
         start_date = str(datetime.fromisoformat(item['from'][:-1]))
         startdate = datetime.fromisoformat(item['from'][:-1])
         start_time = startdate.strftime("%H:%M")+ ":00"
         enddate = startdate + timedelta(minutes=30)
         end_time = enddate.strftime("%H:%M")+ ":00"
         cost = str(item['Cost'])
         minrate = str(MinRate)
         maxrate = str(MaxRate)
         meanrate = str(MeanRate)
         tariff_new += '"'+ run_num +'": "' + start_date + '",' + '"' + cost_num + '": '+ '"' + cost + '",'+ '"' + start_num + '": "' + start_time + '","' + end_num +'": "' + end_time + '",' + '"' + min_rate + '": '+ '"' + minrate + '",'+ '"' + max_rate + '": "' + maxrate +'",'+ '"' + mean_rate + '": "' + meanrate + '",'
    
             
    print(tariff_new[:-1]+' }')

    r.close()

else:
    print('{"rate": "error" }')
    r.close()
