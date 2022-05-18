from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests
import json
from time import sleep
import redis
from order import Order

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

#Give a unique ID for the drone
#===================================================================
myID = "Test"
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
with open('data.json', 'r') as f:
    data = json.load(f)

current_longitude = data['long']
current_latitude = data['lat']
#===================================================================

drone_info = {'id': myID,
                'longitude': current_longitude,
                'latitude': current_latitude,
                'status': 'idle'
            }

# Fill in the IP address of server, and send the initial location of the drone to the SERVER
#===================================================================
SERVER="http://10.11.44.125:5001/drone"
with requests.Session() as session:
    resp = session.post(SERVER, json=drone_info)
#===================================================================

def get_coords(self, order):
    return {'from' : order.coordinatesFrom, 'to' : order.coordinatesTo}


def nmain():
    redis_server = redis.Redis("10.11.44.125", decode_responses=True, charset="unicode_escape", port="6379")
    while True:
        sleep(2)
        nbr = redis_server.llen("OrderQueue")
        if (nbr > 0):
            order = redis_server.lpop("OrderQueue")
            order = json.loads(order, object_hook=Order.from_json)
            coords = get_coords(order)

            from_coord = coords['from']
            to_coord = coords['to']

            subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                '--id', myID
                            ])

# @app.route('/', methods=['POST'])
# def main():
#     redis_server = redis.Redis("10.11.44.125", decode_responses=True, charset="unicode_escape", port="6379")
#     with open('data.json', 'r') as f:
#         data = json.load(f)
#     print("innan coords")
#     coords = request.json
#     order = redis_server.lpop("OrderQueue")
#     order = json.loads(order, object_hook=Order.from_json)
#     print("sending req to drone cool")
#     coords = get_coords(order)
#     print(coords)

#     # Get current longitude and latitude of the drone 
#     #===================================================================
#     current_longitude = data['long']
#     current_latitude = data['lat']
#     #===================================================================
#     from_coord = coords['from']
#     to_coord = coords['to']
#     print("innan subprocess")
#     subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
#                                                  '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
#                                                  '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
#                                                  '--id', myID
#                     ])
#     return 'New route received'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    nmain()

