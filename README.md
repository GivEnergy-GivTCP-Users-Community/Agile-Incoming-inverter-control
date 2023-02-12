# Agile-Incoming-inverter-control
Holding area for automation to control  
Welcome here you will find the elements to create an automation to charge your batteries
If you are using Octopus Agile incoming Tariff.

------------------------------------------------------------------------------------------------------------------------------
	-            If you have already built this and get two errors about missing script                         -
	-           do the following                                                                                                                       -
------------------------------------------------------------------------------------------------------------------------------
Firstly if you have already loaded this automation and got two error messages do the following
Delete agile_solar_forecast_target script go to file editor open up the scripts.yaml
File add 

set_solar_forecast_target:
  alias: agile_solar_forecast_target
  fields:
    target_soc:
      description: the target soc to use
      example: 100
  sequence:
  - service: input_number.set_value
    data:
      value: '{{(states(''sensor.solcast_forecast_remaining_today'') | float(0))}}'
    target:
      entity_id: input_number.target_sol_forecast
  - service: input_number.set_value
    data:
      value: '{{target_soc}}'
    target:
      entity_id: input_number.target_soc
  mode: single

You will find it in the repository labeled  'add this to scripts.yaml'

Validate the Yaml in developers tools and if ok restart HA
It would be beneficial to delete and re build the scripts and automations as we have found that
The GUI sometimes adds its own script name unless the process below is followed
--------------------------------------------------------------------------------------------------------------------------

![image](https://user-images.githubusercontent.com/115955610/218300932-aa2277c6-56fd-4437-afc2-7a7745699664.png)

