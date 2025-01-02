#!/usr/bin/Get_Agile_incomming v2 fix applied value stuck at var 10

# importing the requests library
import requests
import json
from dateutil import tz
from datetime import datetime, timedelta

#setup timezone
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/London')

# api-endpoint
BASE_URL = "https://api.octopus.energy"
##########################################################
### the following you need to find in your octopus account
PRODUCT_CODE = "AGILE-24-10-01"
##########################################################
# change  the "-B" bit to match your region code
REGION = "-B"
##############
TARIFF_CODE = "E-1R-" + PRODUCT_CODE + REGION 
TARIFF_URL = BASE_URL + "/v1/products/" + PRODUCT_CODE + "/electricity-tariffs/" + TARIFF_CODE

# test url get tariffs https://api.octopus.energy/v1/products/. 
#TARIFF_URL = "https://api.octopus.energy/v1/products/."
  
#setting the time
now = datetime.now()+ timedelta(days = 0)
DATEFROM = now.strftime("%Y-%m-%d")+ "T16:00Z"
newdate = now + timedelta(days = 1)
DATETO = newdate.strftime("%Y-%m-%d")+ "T18:00Z"


# parameter items given here
PERIOD_FROM = DATEFROM
PERIOD_TO = DATETO

# defining the outgoing url
URL = TARIFF_URL + "/standard-unit-rates/?" + "period_from=" + PERIOD_FROM + "&period_to=" + PERIOD_TO
#URL = TARIFF_URL
#### debug url #####
#print(URL)
#### end debug ####
  
# sending Get request
r = requests.get(URL)

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
         start_date_tz = datetime.fromisoformat(item['from'][:-1])
         start_date_nz = start_date_tz.replace(tzinfo=from_zone)
         startdate = start_date_nz.astimezone(to_zone)
         start_date = str(startdate.strftime("%Y-%m-%d %H:%M"))
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
