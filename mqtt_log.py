import paho.mqtt.client as mqtt
import time
import subprocess
import serial
from datetime import datetime
import json

ping_command = ["ping 8.8.8.8 -I wwan0 -c1 -w2 -s0","ping 8.8.8.8 -I wlan0 -c1 -w2 -s0","ping 8.8.8.8 -I eth0 -c1 -w2 -s0"]
ping_result_arr = []


def check_signal():
    try:
        ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=5)
        ser.write(b"AT+CSQ\r")  # Attention - Echo disable
        response = ser.read(20)
        # print(response.decode('utf-8'))
        ser.close()
        return response.decode('utf-8')
    except Exception as e:
        return repr(e) + " modem not connected"

def read_temp():
    try:
        temperature_measurement = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
        temperature_measurement = temperature_measurement.decode('utf-8')
        temperature_measurement = str(temperature_measurement).replace('temp=','')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time = str(timestamp)
        temp = f"{temperature_measurement}"
        return temp,time
    except:
        return 'temp error'

def ping():
    #ping_result_arr=[]
    for cmd in ping_command:
        try:
            ping_result = subprocess.check_output(cmd, shell=True, text=True)
            ping_result_arr.append(str(ping_result.strip()))
        except:
            ping_result_arr.append('')

def get_metric():
    try:
        ping_result = subprocess.check_output("ip route", shell=True, text=True)
        return str(ping_result.strip())
    except:
        pass

while True:
    time.sleep(10)
    try:
        broker_address = "broker.hivemq.com" 
        topic = "/adsb/nutech/log"
        client = mqtt.Client(("ADSB-Publisher"+str(time.time())))
        client.connect(broker_address)
        ping_result_arr = []
        ping()
        dict = {
            'time':read_temp()[1],
            'data':{
                'ping':ping_result_arr,
                'temperature':read_temp()[0],
                'modem_status':check_signal(),
                'metric_status':get_metric()
            }
        }
        client.publish(topic, json.dumps(dict))
        client.disconnect()
    except Exception as e:
        print("error ->",e)