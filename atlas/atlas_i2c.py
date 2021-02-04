from atlas_i2c import sensors
sensor = sensors.Sensor("Temperature", 102)
sensor.connect()
response = sensor.query(commands.READ)
print(response.data)
