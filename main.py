import sys
from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import adafruit_bh1750
import time
import board
import digitalio
import adafruit_bmp280
import RPi.GPIO as GPIO
import json
import pigpio
import os
from rpi_lcd import LCD
import socket
import controller_pid
import controller_fuzzy

pid_controller = controller_pid.pid_controller()
fuzzy_controller = controller_fuzzy.controller_fuzzy()


lcd = LCD()
lcd.text("Hum:    Tm:  ", 1, 0)
lcd.text("Lux:", 2, 0)

pi=pigpio.pi()
pi.set_PWM_dutycycle(13, 0)
pi.write(12, 1)
pi.write(23, 0)

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

desired_lux = 1000

with open('static/data/actual_data.json','w') as outfile:
    print("start")
 
delta_time = 0.2
start_time = time.time()
lcd_update_time = 0

data=[]

temp_regulator = True
hum_regulator = False

try:
    while True:

       
        if( (time.time() - start_time) >= delta_time):
            
            config = []
            with open('static/data/config.json','r') as file:
                config = json.load(file)
                desired_lux = float(config[0]['lux'])
                desired_temp = float(config[0]['temp'])
                desired_hum = float(config[0]['hum'])
                file.close()
        
            if not config[0]['start']:
                config[0]['start'] = True
                
                print("config:")
                print("desired lux:" + str(config[0]['lux']))
                print("desired temp:" + str(config[0]['temp']))
                print("desired hum:" + str(config[0]['hum']))
                print("\n")
                pid_controller.reset()
                fuzzy_controller.reset()
                
                pi.set_PWM_dutycycle(13, 0)
               
                sleep(0.8)
                start_time = time.time()
                with open('static/data/actual_data.json','w') as outfile:
                    outfile.close()
                
            with open('static/data/config.json','w') as file:
                json.dump(config,file, indent = 1)
                file.close()
            
            
            dt = time.time()-start_time
            start_time = time.time()
            
            lux = sensor.lux
            hum = (mcp.read_adc(0)/1023.0)*100.0*(5.0/3.3)
            temp = bmp280.temperature
            
            data = []
            
            with open('static/data/actual_data.json','r') as file:
                if os.path.getsize('static/data/actual_data.json') > 0:
                    data = json.load(file)
                    data.append({'Light':round(lux, 2), 'Temperature':round(temp,2), 'Humidity': round(hum,2) , 't': round((data[len(data)-1]['t'] + dt),2)})
                else:
                    data.append({'Light':round(lux, 2), 'Temperature':round(temp,2), 'Humidity': round(hum,2) , 't':0.0})
                    start_time = time.time()
            
            if config[0]['pid']:
                pi.set_PWM_dutycycle(13, 255.0*pid_controller.calculate_output(desired_lux, lux, dt)/100.0)
            else:   
                pi.set_PWM_dutycycle(13, 255.0*fuzzy_controller.calculate_output(desired_lux, lux)/100.0)

            
            if temp_regulator:
                if temp < desired_temp - 2:
                    temp_regulator = False
                    pi.write(12, 0)
            else:
                if temp > desired_temp + 2:
                    temp_regulator = True
                    pi.write(12, 1)
            
            if hum_regulator:
                if hum > desired_hum + 2:
                    hum_regulator = False
                    pi.write(23, 0)
                    print("pompka off")
            else:
                if hum < desired_hum - 2:
                    hum_regulator = True
                    pi.write(23, 1)
                    print("pompka on")
            
            if len(data) == 151:
                data.pop(0)
              
            try:
                with open('static/data/actual_data.json','w') as outfile:
                    json.dump(data,outfile, indent = 1)
            finally:
                outfile.close()
                

            if ( time.time() - lcd_update_time >= 1.0 ):
                lcd.text("Hum:%.0f%s Tm:%.1fC" %(hum,"%", temp), 1, 0)
                lcd.text("Lux:%.2f lx" %(lux), 2, 0)
                lcd_update_time = time.time()
        
except KeyboardInterrupt:
    sys.exit()
