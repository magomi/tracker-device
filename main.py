from machine import I2C, Pin
from umqtt.simple import MQTTClient
import mpu6050
import time

i2c = I2C(scl=Pin(5), sda=Pin(4))
accelerometer = mpu6050.accel(i2c)
c = MQTTClient("umqtt_client", server="192.168.2.128", port=8883, user="tracker-device-01", password="xxxxxxxxxxxxx")
c.connect()

time.sleep(10)

while True:
    values = accelerometer.get_values()
    print(values)
    message_template = '''
    {{
        "gyro": {{
            "x": "{}", 
            "y": "{}", 
            "z": "{}"
        }}, 
        "acc": {{
            "x": "{}", 
            "y": "{}", 
            "z": "{}"
        }}
    }}'''
    message = message_template.format(values["GyX"], values["GyY"], values["GyZ"],
                                      values["AcX"], values["AcY"], values["AcZ"])
    c.publish("tracker/tracker-dev-01/data/position", message)
    time.sleep(1)


c.disconnect()
