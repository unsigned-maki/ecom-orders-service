import json
import database
from flask import Flask, request

app = Flask(__name__)


def not_found():
    return json.dumps({"success": False, "code": 404, "message": "Not Found"})


def method_not_allowed():
    return json.dumps({"success": False, "code": 405, "message": "Method Not Allowed"})


def ok():
    return json.dumps({"success": True, "code": 200, "message": "OK"})


@app.route("/customer", methods=["GET", "POST"])
def customer_handler():
    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "cutomers": database.Customers.to_list()})
    elif request.method == "POST":
        database.NewCustomer(**request.form)
        return ok()
    else:
        return method_not_allowed()


@app.route("/customer/<id_>", methods=["GET", "PATCH", "DELETE"])
def customer_handler_id(id_):
    customer = database.Customer.from_id(id_)

    if not customer:
        return not_found()

    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "customer": customer.to_dict()})
    elif request.method == "PATCH":
        customer.patch(**request.form)
        customer.update()
        return ok()
    elif request.method == "DELETE":
        customer.remove()
        return ok()
    else:
        return method_not_allowed()


@app.route("/order", methods=["GET", "POST"])
def product_handler():
    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "orders": database.Orders.to_list()})
    elif request.method == "POST":
        database.NewOrder(**request.form)
        return ok()
    else:
        return method_not_allowed()


@app.route("/order/<id_>", methods=["GET", "PATCH", "DELETE"])
def product_handler_id(id_):
    order = database.Order.from_id(id_)
    
    if not order:
        return not_found()

    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "order": order.to_dict()})
    elif request.method == "PATCH":
        order.patch(**request.form)
        order.update()
        return ok()
    elif request.method == "DELETE":
        order.remove()
        return ok()
    else:
        return method_not_allowed()


if __name__ == '__main__':
    app.run()
