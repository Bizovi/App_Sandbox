"""The web service only takes care of typical web-server stuff. Request-response

TODO(Mihai): a read-only endpoint: repo.get() in the flask handler. Note that 
reads vs writes is quite a big topic and has its own pattern.
"""

from datetime import datetime
from flask import Flask, jsonify, request

from allocation.domain import model
from allocation.adapters import orm
from allocation.service_layer import services, unit_of_work


app = Flask(__name__)
orm.start_mappers()


@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json.get("eta")
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    
    services.add_batch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta,
        unit_of_work.SqlAlchemyUnitOfWork(),  # dependency injection (only one)
    )

    return "OK", 201


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            unit_of_work.SqlAlchemyUnitOfWork(),   
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201