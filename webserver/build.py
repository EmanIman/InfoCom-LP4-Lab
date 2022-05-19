from os import fdopen
from flask import Flask, render_template, request
from flask.json import jsonify
# from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this so that you can connect to your redis server
# ===============================================
redis_server = redis.Redis("localhost", decode_responses=True, charset="unicode_escape")
# ===============================================

# Translate OSM coordinate (longitude, latitude) to SVG coordinates (x,y).
# Input coords_osm is a tuple (longitude, latitude).
def translate(coords_osm):
    x_osm_lim = (13.143390664, 13.257501336)
    y_osm_lim = (55.678138854000004, 55.734680845999996)

    x_svg_lim = (212.155699, 968.644301)
    y_svg_lim = (103.68, 768.96)

    x_osm = coords_osm[0]
    y_osm = coords_osm[1]

    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (x_osm - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - y_osm) + y_svg_lim[0]

    return x_svg, y_svg

@app.route('/', methods=['GET'])
def map():
    return render_template('index.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    #=============================================================================================================================================
    # Get the information of all the drones from redis server and update the dictionary `drone_dict' to create the response 
    # drone_dict should have the following format:
    # e.g if there are two drones in the system with IDs: DRONE1 and DRONE2
    # drone_dict = {'DRONE_1':{'longitude': drone1_logitude_svg, 'latitude': drone1_logitude_svg, 'status': drone1_status},
    #               'DRONE_2': {'longitude': drone2_logitude_svg, 'latitude': drone2_logitude_svg, 'status': drone2_status}
    #              }
    # use function translate() to covert the coodirnates to svg coordinates
    #=============================================================================================================================================
    drone_dict = {}
    # drones = ["Test", "drone124"]
    drones = ["drone124", "Test"]
    
    for d in drones:
        info = redis_server.get(d)
        if info == None:
            info = {'long': 13.21008, 'lat': 55.71106, 'status': 'idle', 'id': d}
            redis_server.set(f"{d}", json.dumps(info))
        else:
            info = json.loads(info)
        translated = translate((float(info['long']), float(info['lat'])))
        drone_dict[d] = {'longitude': translated[0], 'latitude': translated[1], 'status': info['status']}



    return jsonify(drone_dict)

@app.route('/get_order/<order_uuid>', methods=['GET'])
def get_order(order_uuid):
    # if order is being processed: return drone json stuff
    # else: 
    #return(http.HTTPStatus.NO_CONTENT) # kanske inte funkar
    return('', 204)

@app.route('/track/<order_uuid>', methods=['GET'])
def track(order_uuid):
    return render_template('track.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')