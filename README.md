# Agile-Incoming-inverter-control
Holding area for automation to control  

Agile Incoming Automation

11 February 2023
09:26

Welcome here you will find the elements to create an automation to charge your batteries
If you are using Octopus Agile incoming Tariff.

To create the full automation you will have to follow these details and complete the required steps
In this order.

Step 1 using file editor create a new directory "pyscripts" into this directory save the following
File get_agile_incoming_ordered.py 
You will then have to edit the file at line 22 and then save it
# parameter items given here
APIKEY="your octopus api key"

Step 2 you will have to add the following files into the config directory
input_boolean.yaml
input_number.yaml
input_text.yaml

Step 3 edit the secrets.yaml and add the details as in the following file
secrets.yaml

Replacing the Your@gmail.com with your actual email address at gmail.com

Step 4

Edit the configuration yamal add the details that are in the supplied configuration.yaml
configuration.yaml

Alter the entry recipient to be where you want the email address you want the email to 
go to
notify:
  - name: "Give_Charge"
    platform: smtp
    server: "smtp.gmail.com"
    port: 587
    timeout: 15
    sender: !secret email_sender
    encryption: starttls
    username: !secret email_user
    password: !secret email_password
    recipient:
      - "your email address"
    sender_name: "Givenergy Inverter"



From <https://github.com/GivEnergy-GivTCP-Users-Community/Agile-Incoming-inverter-control/blob/main/configuration.yaml> 



Step five go to developers tools YAML and press the check configuration link you should see


 you should see the following if you have done it correctly



Now press the restart link 



Step six  go to settings, automations and scripts and add the scripts
By copying the contents of the script files .

Like this







Add the contents of the first script after removing the default script settings



To the new script




And a save button will come up press it until you have built all of the scripts

Step 7 do the same for automations

Remembering where ever you see 
**your inverter id**
Change it to your inverters ID

Step 8 build the dashboard
Go to settings dashboard


Add dashboard dashboard


Add the title Control




And then press create

Click the open button next to the newly created dashboard in the list


Click the 3 dots to right corner


Edit dashboard


Select start with an empty dashboard and then press take control



Click the 3 dots again and select raw configuration editor



Copy all the code from 
Octopus Agile Control dashboard.yaml

And save

Last steps go to the newly created automation 
Load_Agile and run it 

You should see the following


And if you click on the calculator icon





If you select a price weight it will filter out the more expensive of the ten available rates
This is so you can direct your inverter to just use the cheapest possible rates set the slider
To 2 and see what becomes enabled disabled.

Soc limit will automatically be set by the amount of expected solar energy to be 
Generated remaining for today, this is updated as the session becomes live and is used by
The session control to decide to charge or not.

You can edit the script agile_sol_check_control and set your 
own values to use.
alias: agile_sol_check_control
sequence:
  - variables:
      target_soc: >-
        {% set solar_forecast = states(entity_solar_forecast)|float %} {% if
        solar_forecast > 21.0 %} 10 {% elif solar_forecast > 18.0 %} 20 {% elif
        solar_forecast > 15.0 %} 40{% elif solar_forecast > 13.0 %} 60 {% elif
        solar_forecast > 11.0 %} 70 {% elif solar_forecast > 9.0 %} 80 {% elif
        solar_forecast > 7.0 %} 90 {% else %} 100 {% endif %}
- service: script.set_solar_forecast_target
    data:
      target_soc: "{{ target_soc | float }} "
variables:
  entity_solar_forecast: sensor.solcast_forecast_remaining_today
mode: single

From <https://github.com/GivEnergy-GivTCP-Users-Community/Agile-Incoming-inverter-control/blob/main/script%20agile_sol_check_control.yml> 


If you don’t want emails you can set this in the script agile_charge_battery


      - service: script.agile_fail_email
        data:
          emailmessage: session is negative force charge enabled
          emailtitle: "{{title}}"
          notification_id: "{{notification_id}}"
          notification_type: set this to gen from email

![image](https://user-images.githubusercontent.com/115955610/218252989-66fad905-fb14-453d-9728-4beb362de0c5.png)
