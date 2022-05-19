from flask import Flask, render_template
from flask.json import jsonify
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


@app.route('/get_order/<order_uuid>', methods=['GET'])
def get_order(order_uuid):
    drone_dict = {}
    drones = ["drone124", "Test"]
    
    for d in drones:
        drone_info = redis_server.get(d)
        drone_info = json.loads(drone_info)

        if drone_info['uuid'] == order_uuid:
            translated = translate((float(drone_info['long']), float(drone_info['lat'])))
            drone_dict[d] = {'longitude': translated[0], 'latitude': translated[1], 'status': drone_info['status'], 'uuid': drone_info['uuid']}

    return jsonify(drone_dict)

@app.route('/track/<order_uuid>', methods=['GET'])
def track(order_uuid):
    return render_template('track.html', order_uuid=order_uuid)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5003')