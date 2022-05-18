import redis
import json
import requests
from order import Order
from time import sleep

class DroneCommunicator:

    def __init__(self):
        self.redis_server = redis.Redis("localhost", decode_responses=True, charset="unicode_escape")
    
    def send_request(self, drone_url):
        with requests.Session() as session:
            resp = session.post(drone_url)

    def get_coords(self, order):
        return {'from' : order.coordinatesFrom, 'to' : order.coordinatesTo}

    def queueLoop(self):
        nbr = self.redis_server.llen("OrderQueue")
        print(f"Idle loop, Orders In Queue: {nbr}")
        if (self.redis_server.llen("OrderQueue") > 0):
            drones = {"Test": '10.11.44.126', "drone124": '10.11.44.124'}
            drone = None
            for k, v in drones.items():
                print(k)
                info = self.redis_server.get(k)
                print(info)
                if info != None:
                    info = json.loads(info)
                    if info['status'] == 'idle':
                        drone = v
                        break
            
            if drone != None:
                self.send_request("http://" + drone + ":5000")





# Old stuff

# from concurrent.futures import thread
# import redis
# import json
# import requests
# from order import Order
# from time import sleep
# import threading

# class DroneCommunicator:
    
#     def __init__(self):
#         self.redis_server = redis.Redis("localhost", decode_responses=True, charset="unicode_escape")

#     def send_request(self, drone_url, coords):
#         with requests.Session() as session:
#             resp = session.post(drone_url, json=coords)

#     def get_coords(self, order):
#         return {'from' : order.coordinatesFrom, 'to' : order.coordinatesTo}

#     def queueLoop(self):
#         while True:
#             sleep(3)
#             nbr = self.redis_server.llen("OrderQueue")
#             print(f"Idle loop, Orders In Queue: {nbr}")
#             if (nbr > 0):
#                 drones = {"Test": '10.11.44.126', "drone124": '10.11.44.124'}
#                 drone_ip = None
#                 for k, v in drones.items():
#                     print(k)
#                     drone_info = self.redis_server.get(k)
#                     print(drone_info)
#                     if drone_info != None:
#                         drone_info = json.loads(drone_info)
#                         if drone_info['status'] == 'idle':
#                             drone_ip = v
#                             break
                
#                 if drone_ip != None:
#                     order = self.redis_server.lpop("OrderQueue")
#                     order = json.loads(order, object_hook=Order.from_json)
#                     print("sending req to drone cool")
#                     print(order.coordinatesFrom)
#                     coords = self.get_coords(order)
#                     print(coords)
#                     # self.send_request("http://" + drone_ip + ":5000", coords)
#                     t = threading.Thread(target=self.send_request, args=["http://" + drone_ip + ":5000", coords])
#                     t.start()




if __name__ == "__main__":
    dc = DroneCommunicator()
    dc.queueLoop()
