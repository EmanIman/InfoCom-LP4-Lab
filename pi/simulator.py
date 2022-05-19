import math
import requests
import argparse
import json
from time import sleep


def getMovement(src, dst):
    speed = 0.0001          # divide by 10 to get back original speed
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    longitude_move = speed * ((dst_x - x) / direction )
    latitude_move = speed * ((dst_y - y) / direction )
    return longitude_move, latitude_move


def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)


def send_location(SERVER_URL, id, drone_coords, status):
    with requests.Session() as session:
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                       'status': status,
                       'uuid': uuid
                    }
        resp = session.post(SERVER_URL, json=drone_info)


def distance(_fr, _to):
    _dist = ((_to[0] - _fr[0])**2 + (_to[1] - _fr[1])**2)*10**6
    return _dist

    
def run(id, current_coords, from_coords, to_coords, SERVER_URL):
    drone_coords = current_coords

    # Move from current_coords to from_coords 
    d_long, d_la =  getMovement(drone_coords, from_coords)
    while distance(drone_coords, from_coords) > 0.0008:      #change back distance
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='busy')
        sleep(0.1)

    # we have arrived to from address led to waiting, and play sound effect and await joystick input to continue
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='waiting')


    # Move from from_coords to to_coords
    d_long, d_la =  getMovement(drone_coords, to_coords)
    while distance(drone_coords, to_coords) > 0.0008:  #change back distance
        
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        
        send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='busy')
        
        sleep(0.1)

    # when we have arrived led to waiting symbol and sound effect await joystick input to continue
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='waiting')
    

    # Stop and update status to database
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='idle')
    
    return drone_coords[0], drone_coords[1]
   
   
if __name__ == "__main__":
    # Fill in the IP address of server, in order to location of the drone to the SERVER
    #===================================================================
    SERVER_URL = "http://10.11.44.125:5001/drone"
    #===================================================================
    print("in sim")

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--id", help ='drones ID' ,type=str)
    parser.add_argument("--uuid", help='order uuid', type=str)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    uuid = args.uuid

    print(current_coords, from_coords, to_coords)
    drone_long, drone_lat = run(args.id, current_coords, from_coords, to_coords, SERVER_URL)
    # drone_long and drone_lat is the final location when drlivery is completed, find a way save the value, and use it for the initial coordinates of next delivery
    #=============================================================================
    data = {'long' : drone_long, 'lat' : drone_lat}
    with open('data.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
