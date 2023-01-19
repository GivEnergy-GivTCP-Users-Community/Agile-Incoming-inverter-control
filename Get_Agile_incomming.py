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
now = datetime.now()+ timedelta(days = 1)
DATEFROM = now.strftime("%Y-%m-%d")+ "T00:00Z"
newdate = now + timedelta(days = 2)
DATETO = newdate.strftime("%Y-%m-%d")+ "T00:00Z"

# parameter items given here
APIKEY = "add your api key here"
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
    #print(data)
    
# create final json output
    tariff_new = '{'
    y = 0
    for item in data:
         y = y + 1
         run_num = 'Run_number' +str(y)
         cost_num = 'cost_number' +str(y) 
         start_date = str(datetime.fromisoformat(item['from'][:-1]))
         cost = str(item['Cost'])
         tariff_new += '"'+ run_num +'": "' + start_date + '",' + '"' + cost_num + '": '+ '"' + cost + '",'

             
    print(tariff_new[:-1]+'}')

    r.close()

else:
    print('{"rate": "error" }')
    r.close()
