import uuid, json

class Order:
  def __init__(self, coordinatesFrom, coordinatesTo, order_uuid, status, drone):
      self.coordinatesFrom = coordinatesFrom
      self.coordinatesTo = coordinatesTo
      self.order_uuid = order_uuid
      # when an order is placed we should check if there is an available drone, if so set status and drone accordingly
      self.status = status
      self.drone = drone

  @classmethod
  def from_coords(cls, coords):
      return cls(coordinatesFrom=coords['from'], coordinatesTo=coords['to'],
          order_uuid=str(uuid.uuid4()), status="queue", drone=None)

  def get_coords(self):
      return {'from' : self.coordinatesFrom, 'to' : self.coordinatesTo}

  def __iter__(self):
      yield from {
          "coordinatesFrom": self.coordinatesFrom,
          "coordinatesTo": self.coordinatesTo,
          "order_uuid": self.order_uuid,
          "status": self.status,
          "drone": self.drone
      }.items()

  def __str__(self):
      return json.dumps(dict(self), ensure_ascii=False)

  def __repr__(self):
      return self.__str__()

  def to_json(self):
      return self.__str__()
    
  @staticmethod
  def from_json(json_dct):
      return Order(json_dct['coordinatesFrom'],
                  json_dct['coordinatesTo'], json_dct['order_uuid'],
                  json_dct['status'], json_dct['drone'])