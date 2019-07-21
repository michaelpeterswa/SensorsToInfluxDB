import argparse
import time
import datetime
from influxdb import InfluxDBClient
import serial
import math



def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    ser = serial.Serial('/dev/ttyACM0',9600)
    user = 'root'
    password = 'root'
    dbname = 'arduino_sensors'
    #dbuser = 'admin'
    #dbuser_password = 'admin'
    #query = 'select value from light;'
    firstRun = False

    while True:

        '''currentTime = int(time.time())'''
        currentTime = datetime.datetime.utcnow().isoformat()
        temperature = float(ser.readline())
        pressure = float(ser.readline())
        humidity = float(ser.readline())
        gasses = float(ser.readline())
        light = float(ser.readline())


        json_body = [
            {
                "measurement": "environment",
                "tags": {
                    "host": "raspberrypi",
                    "region": "us-west"
                },
                "time": currentTime,
                "fields": {
                    "temperature": temperature,
                    "pressure": pressure,
                    "humidity": humidity,
                    "gasses": gasses,
                    "light": light,
                }
            }
        ]

        client = InfluxDBClient(host, port, user, password, dbname)

        if firstRun == False:
            print("Create database: " + dbname)
            client.create_database(dbname)
            firstRun = True

        """print("Switch user: " + dbuser)
        client.switch_user(dbuser, dbuser_password)"""

        """print("Write points: {0}")"""
        client.write_points(json_body)

        """print("Querying data: " + query)
        result = client.query(query)

        print("Result: {0}".format(result))"""

        """print("Switch user: " + user)
        client.switch_user(user, password)"""

        """print("Drop database: " + dbname)
        client.drop_database(dbname)"""


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
