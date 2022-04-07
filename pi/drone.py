from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests
import json
# from sense_hat import SenseHat


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# sense = SenseHat()
g = (0, 255, 0)
w = (255, 255, 255)

idle_pixels = [
    g, g, g, g, g, g, g, w,
    g, g, g, g, g, g, w, w,
    g, g, g, g, g, w, w, g,
    w, g, g, g, w, w, g, g,
    w, w, g, w, w, g, g, g,
    g, w, w, w, g, g, g, g,
    g, g, w, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
]

# def display_status(pixels):
#     sense.set_pixels(pixels)

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

# drone starts set senshat led to be green/idle symbol
# display_status(idle_pixels)

@app.route('/', methods=['POST'])
def main():
    with open('data.json', 'r') as f:
        data = json.load(f)
    print("innan coords")
    coords = request.json
    # Get current longitude and latitude of the drone 
    #===================================================================
    current_longitude = data['long']
    current_latitude = data['lat']
    #===================================================================
    from_coord = coords['from']
    to_coord = coords['to']
    print("innan subprocess")
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
