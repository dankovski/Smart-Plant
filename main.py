import sys
from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import adafruit_bh1750
import time
import board
import adafruit_bmp280
import json
import pigpio
import os
from rpi_lcd import LCD
import controller_pid
import controller_fuzzy
from datetime import datetime, timedelta
import i2c_lcd
lcd = i2c_lcd.lcd()



lcd.lcd_display_string("Hum:    Tm:  ", 1)
lcd.lcd_display_string("Lux:", 2)

pi=pigpio.pi()
pi.set_PWM_dutycycle(13, 0)
pi.write(12, 1)
pi.write(23, 0)

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

pid_controller = controller_pid.pid_controller()
fuzzy_controller = controller_fuzzy.controller_fuzzy()


desired_lux = 1000
lcd_update_time = 0
delta_time = 0.0

temp_regulator = True
hum_regulator = False

actual_data = []
config = []
start_time = time.time()

next_update = datetime.now() + timedelta(hours=1)
next_update = next_update.replace(minute=0)
next_update = next_update.replace(second=0)

try:
    with open('static/data/actual_data.json','w') as outfile:
        outfile.close()
except:
    print("Can't open actual_data.json")


try:
    with open('static/data/actual_data_pid.json','w') as outfile:
        outfile.close()
except:
    print("Can't open actual_actual_data_pid.json")

try:
    with open('static/data/actual_data_fuzzy.json','w') as outfile:
        outfile.close()
except:
    print("Can't open actual_actual_data_fuzzy.json")

print("start")

try:
    while True:
        
        if( (time.time() - start_time) >= delta_time):
            #calculating delta time
            dt = time.time()-start_time
            start_time = time.time()
            #print(dt)
            if dt > delta_time:
                dt=delta_time
            
            #reading config
            try:
                with open('static/data/config.json','r') as file:
                    config = json.load(file)
                    file.close()
                    desired_lux = float(config[0]['lux'])
                    desired_temp = float(config[0]['temp'])
                    desired_hum = float(config[0]['hum'])
                    delta_time = float(config[0]['dt'])
                    samples = float(config[0]['samples'])
            except:
                print("Can't open config.json")
            
            #restart
            if not config[0]['start']:
                config[0]['start'] = True
                print("config:")
                print("desired lux:" + str(config[0]['lux']))
                print("desired temp:" + str(config[0]['temp']))
                print("desired hum:" + str(config[0]['hum']))
                print("pid:" + str(config[0]['pid']))
                print("\n")
                
                pid_controller.reset()
                fuzzy_controller.reset()
                
                pi.set_PWM_dutycycle(13, 0)
               
                sleep(0.8)
                start_time = time.time()
                
                try:
                    with open('static/data/actual_data.json','w') as outfile:
                        outfile.close()
                except:
                    print("Can't open actual_data.json")
                
                
                if config[0]['pid']:
                    try:
                        with open('static/data/actual_data_pid.json','w') as outfile:
                            outfile.close()
                    except:
                        print("Can't open actual_actual_data_pid.json")
                else:
                    try:
                        with open('static/data/actual_data_fuzzy.json','w') as outfile:
                            outfile.close()
                    except:
                        print("Can't open actual_actual_data_fuzzy.json")
                  
                try:
                    with open('static/data/config.json','w') as file:
                        json.dump(config,file, indent = 1)
                        file.close()
                except:
                    print("Can't open config.json")
        
            #reading data from sensors
            lux = sensor.lux
            hum = (mcp.read_adc(0)/1024.0)*100.0*(5.0/3.3)
            temp = bmp280.temperature
            
  
            #working regulators
            actual_data = []
            output = []
            
            if config[0]['pid']:
                output = pid_controller.calculate_output(desired_lux, lux, dt)
                pi.set_PWM_dutycycle(13, 255.0*output/100.0)
                try:
                    with open('static/data/actual_data_pid.json','r') as file:
                        if os.path.getsize('static/data/actual_data_pid.json') > 0:
                            actual_data = json.load(file)
                            actual_data.append({'Light':round(lux, 2), 't': round((actual_data[len(actual_data)-1]['t'] + dt),2), 'pwm': round(output, 2)})
                        else:
                            actual_data.append({'Light':round(lux, 2), 't':0.0, 'pwm': 0})
                    file.close()
                except:
                    print("Can't load actual_data_pid.json")
                    
                if len(actual_data) == (samples + 2):
                    actual_data.pop()

                try:
                    with open('static/data/actual_data_pid.json','w') as outfile:
                        json.dump(actual_data,outfile, indent = 1)
                        outfile.close()
                except:
                    print("Can't open actual_data_pid.json")
                
            else:
                output=fuzzy_controller.calculate_output(desired_lux, lux)
                pi.set_PWM_dutycycle(13, 255.0*output/100.0)
                try:
                    with open('static/data/actual_data_fuzzy.json','r') as file:
                        if os.path.getsize('static/data/actual_data_fuzzy.json') > 0:
                            actual_data = json.load(file)
                            actual_data.append({'Light':round(lux, 2), 't': round((actual_data[len(actual_data)-1]['t'] + dt),2), 'pwm': round(output,2)})
                        else:
                            actual_data.append({'Light':round(lux, 2), 't':0.0, 'pwm': 0})
                    file.close()
                except:
                    print("Can't open actual_data_fuzzy.json")
                    
                if len(actual_data) == (samples + 2):
                    actual_data.pop()
                    
                try:
                    with open('static/data/actual_data_fuzzy.json','w') as outfile:
                        json.dump(actual_data,outfile, indent = 1)
                        outfile.close()
                except:
                    print("Can't open actual_data_fuzzy.json")
                
            if temp_regulator:
                if temp < desired_temp - 0.2:
                    temp_regulator = False
                    pi.write(12, 0)
            else:
                if temp > desired_temp + 0.2:
                    temp_regulator = True
                    pi.write(12, 1)
            if hum_regulator:
                if hum > desired_hum + 2:
                    hum_regulator = False
                    pi.write(23, 0)
                    print("pump off")
            else:
                if hum < desired_hum - 2:
                    hum_regulator = True
                    pi.write(23, 1)
                    print("pump on")
            
            actual_data = []
            #writing actual data
            try:
                with open('static/data/actual_data.json','r') as file:
                    if os.path.getsize('static/data/actual_data.json') > 0:
                        actual_data = json.load(file)
                        actual_data.append({'Light':round(lux, 2), 'Temperature':round(temp,2), 'Humidity': round(hum,2) , 't': round((actual_data[len(actual_data)-1]['t'] + dt),2), 'pwm': output})
                    else:
                        actual_data.append({'Light':round(lux, 2), 'Temperature':round(temp,2), 'Humidity': round(hum,2) , 't':0.0, 'pwm': 0.0})
                    file.close()
            except:
                print("Can't open actual_data.json")
                
            if len(actual_data) == (samples + 2):
                actual_data.pop(0)
                
            try:
                with open('static/data/actual_data.json','w') as outfile:
                    json.dump(actual_data,outfile, indent = 1)
            finally:
                outfile.close()
                  
            #historical data update
            if datetime.now() > next_update:
                historical_data = []
                date = str(datetime.now().day) + "." + str(datetime.now().month)+" "+str(datetime.now().hour)+":00"
                print("Historical data has been saved at "+ date)
                
                try:
                    with open('static/data/historical_data.json','r') as file:
                        if os.path.getsize('static/data/historical_data.json') > 0:
                            historical_data = json.load(file)
                        file.close()
                        
                        historical_data.append({'Light':round(lux, 2), 'Temperature':round(temp,2), 'Humidity': round(hum,2), 'date':date})
                        
                except:
                    print("Can't read data from historical_data.json")
                    
                if len(historical_data) == (25):
                    historical_data.pop(0)
                
                try:
                    with open('static/data/historical_data.json','w') as outfile:
                        json.dump(historical_data,outfile, indent = 1)
                        outfile.close()
                except:
                    print("Can't open historical_data.json")
                
                next_update = datetime.now() + timedelta(hours=1)
                next_update = next_update.replace(minute=0)
                next_update = next_update.replace(second=0)
                
            
            #lcd update
            if ( time.time() - lcd_update_time >= 3.0 ):           
                lcd.lcd_display_string("Hum:%.0f%s Tm:%.1fC" %(hum,"%", temp), 1)
                lcd.lcd_display_string("Lux:%.2f lx   " %(lux), 2)
                lcd_update_time = time.time()
                
                
                

except KeyboardInterrupt:
    print("finish")
    lcd.lcd_display_string("Hum:    Tm:     ", 1)
    lcd.lcd_display_string("Lux:          ", 2)

    pi.set_PWM_dutycycle(13, 0)
    pi.write(12, 0)
    pi.write(23, 0)
    
    sys.exit()
