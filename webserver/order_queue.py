import queue
import socket
import threading
from time import sleep
import requests
import json
import redis
from order import Order

def send_request(drone_url, coords):
    with requests.Session() as session:
        resp = session.post(drone_url, json=coords)

def get_coords(order):
    return {'from' : order.coordinatesFrom, 'to' : order.coordinatesTo}


def send_order(redis_server):
    while True:
        sleep(1)
        drones = {"Test": '10.11.44.126', "drone124": '10.11.44.124'}
        drone_ip = None
        for k, v in drones.items():
            print(k)
            drone_info = redis_server.get(k)
            # print(drone_info)
            
            if drone_info != None:    
                drone_info = json.loads(drone_info)

                if drone_info['status'] == 'idle':
                    if not q.empty(): 
                        order = q.get()
                        
                        print("\n -------------------------- \n Current Queue After Get")
                        print(list(q.queue))    
                        
                        drone_ip = v
                        coords = get_coords(order)
                        print(f"\nFound Drone: {drone_info['id']} sending order to it\n")
                        send_request("http://" + drone_ip + ":5000", coords)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(3)
    
    redis_server = redis.Redis("localhost", decode_responses=True, charset="unicode_escape")
    t = threading.Thread(target=send_order, args=(redis_server,))
    t.start()

    while True:
        clientsocket, address = s.accept()
        print(f"connection from {address}")

        order = clientsocket.recv(1024)
        print("\n --------------------------------------------------------------------------- \n Order: \n")
        print(order)

        order = order.decode()
        order = json.loads(order, object_hook=Order.from_json)
        q.put(order)
        print("\n -------------------------- \n Current Queue")
        print(list(q.queue))




if __name__ == '__main__':
    q = queue.Queue()
    main()







"""

Old garbage code might need it for backup tho

def send_order(redis_server):
    while True:
        sleep(1)
        if not q.empty():
            print("\n -------------------------- \n Current Queue")
            print(list(q.queue))
            order = q.get()

            drones = {"Test": '10.11.44.126', "drone124": '10.11.44.124'}
            drone_ip = None
            for k, v in drones.items():
                print(k)
                drone_info = redis_server.get(k)
                print(drone_info)
                
                if drone_info == None:
                    break    

                drone_info = json.loads(drone_info)
                if drone_info['status'] == 'idle':
                    drone_ip = v
                    break

                coords = get_coords(order)
                send_request("http://" + drone_ip + ":5000", coords)
"""