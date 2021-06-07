import json
import pymongo
import os
from utils import generate_uid

client = pymongo.MongoClient(os.getenv("MONGO_DB"))
database = client["Ecom"]
customers = database["customers"]
orders = database["orders"]


class Customer:

    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", generate_uid())
        self.id = self.__id
        self.email = kwargs.get("email", "Unknown")
        self.ip = kwargs.get("ip", "Unknown")
        self.fname = kwargs.get("fname", "None")
        self.lname = kwargs.get("lname", "None")
        self.country = kwargs.get("country", "None")
        self.city = kwargs.get("city", "None")
        self.zip = kwargs.get("zip", 0)
        self.state = kwargs.get("state", "None")

    @staticmethod
    def from_id(id_):
        result = customers.find({"id": id_})

        if result.count() > 0:
            return CursorCustomer(result[0])

        return False

    def patch(self, **kwargs):
        self.email = kwargs.get("email", self.email)
        self.ip = kwargs.get("ip", self.ip)
        self.fname = kwargs.get("fname", self.fname)
        self.lname = kwargs.get("lname", self.lname)
        self.country = kwargs.get("country", self.country)
        self.city = kwargs.get("city", self.city)
        self.zip = kwargs.get("zip", self.zip)
        self.state = kwargs.get("state", self.state)

    def to_dict(self):
        return {"id": self.__id,
                "email": self.email,
                "ip": self.ip,
                "fname": self.fname,
                "lname": self.lname,
                "country": self.country,
                "city": self.city,
                "zip": self.zip,
                "state": self.state}

    def serialize(self):
        return json.dumps(self.to_dict)


class CursorCustomer(Customer):

    def __init__(self, cursor: pymongo.cursor.Cursor):
        super().__init__(id=cursor["id"],
                         email=cursor["email"],
                         ip=cursor["ip"],
                         fname=cursor["fname"],
                         lname=cursor["lname"],
                         country=cursor["country"],
                         city=cursor["city"],
                         zip=cursor["zip"],
                         state=cursor["state"])

    def update(self):
        customers.update_many({"id": self.id}, {"$set": {"email": self.email,
                                                         "ip": self.ip,
                                                         "fname": self.fname,
                                                         "lname": self.lname,
                                                         "country": self.country,
                                                         "city": self.city,
                                                         "zip": self.zip,
                                                         "state": self.state}})

    def remove(self):
        customers.delete_many({"id": self.id})


class NewCustomer(CursorCustomer):

    def __init__(self, **kwargs):
        uid = generate_uid()

        customers.insert_one({"id": uid,
                             "email": kwargs.get("email", "Unknown"),
                             "ip": kwargs.get("ip", "Unknown"),
                             "fname": kwargs.get("fname", "None"),
                             "lname": kwargs.get("lname", "None"),
                             "country": kwargs.get("country", "None"),
                             "city": kwargs.get("city", "None"),
                             "zip": kwargs.get("zip", 0),
                             "state": kwargs.get("state", "None")})

        super().__init__(customers.find_one({"id": uid}))


class Customers:

    @staticmethod
    def to_list():
        customers_list = list()

        for customer in customers.find():
            customers_list.append(CursorOrder(customer).to_dict())

        return customers_list

    @staticmethod
    def serialize():
        return json.dumps(Customers.to_list())


class Order:

    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", generate_uid())
        self.id = self.__id
        self.method = kwargs.get("method", "None")
        self.customer = kwargs.get("customer", "Unknown")
        self.product = kwargs.get("product", "Unknown")
        self.status = kwargs.get("status", "pending")
        self.item = kwargs.get("item", "None")

    @staticmethod
    def from_id(id_):
        result = orders.find({"id": id_})

        if result.count() > 0:
            return CursorOrder(result[0])

        return False

    def patch(self, **kwargs):
        self.method = kwargs.get("method", self.method)
        self.customer = kwargs.get("customer", self.customer)
        self.product = kwargs.get("product", self.product)
        self.status = kwargs.get("status", self.status)
        self.item = kwargs.get("item", self.item)

    def to_dict(self):
        return {"id": self.__id,
                "method": self.method,
                "customer": self.customer,
                "product": self.product,
                "status": self.status,
                "item": self.item}

    def serialize(self):
        return json.dumps(self.to_dict)


class CursorOrder(Order):

    def __init__(self, cursor: pymongo.cursor.Cursor):
        super().__init__(id=cursor["id"],
                         method=cursor["method"],
                         customer=cursor["customer"],
                         product=cursor["product"],
                         status=cursor["status"],
                         item=cursor["item"])

    def update(self):
        if self.method not in ["None", "paypal", "crypto"]:
            self.method = "None"

        if self.customer not in ["done", "pending", "canceled", "awaiting payment"]:
            self.customer = "pending"

        orders.update_many({"id": self.id}, {"$set": {"method": self.method,
                                                        "customer": self.customer,
                                                         "product": self.product,
                                                         "status": self.status,
                                                         "item": self.item}})

    def remove(self):
        orders.delete_many({"id": self.id})


class NewOrder(CursorOrder):

    def __init__(self, **kwargs):
        uid = generate_uid()

        if kwargs.get("method", "None") not in ["None", "paypal", "crypto"]:
            kwargs["method"] = "None"

        if kwargs.get("customers", "pending") not in ["done", "pending", "canceled", "awaiting payment"]:
            kwargs["customers"] = "pending"

        orders.insert_one({"id": uid,
                             "method": kwargs.get("method", "None"),
                             "customer": kwargs.get("customer", "Unknown"),
                             "product": kwargs.get("product", "Unknown"),
                             "status": kwargs.get("status", "pending"),
                             "item": kwargs.get("item", "None")})

        super().__init__(orders.find_one({"id": uid}))


class Orders:

    @staticmethod
    def to_list():
        order_list = list()

        for order in orders.find():
            order_list.append(CursorOrder(order).to_dict())

        return order_list

    @staticmethod
    def serialize():
        return json.dumps(Orders.to_list())

