"""The web service only takes care of typical web-server stuff. Request-response

TODO(Mihai): a read-only endpoint: repo.get() in the flask handler. Note that 
reads vs writes is quite a big topic and has its own pattern.
"""

from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from allocation.domain import model
from allocation.adapters import orm, repository
from allocation.service_layer import services


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/add_batch", methods=["POST"])
def add_batch():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    eta = request.json.get("eta")
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    
    services.add_batch(
        request.json["ref"], request.json["sku"], request.json["qty"],
        eta, repo, session  # dependency injections
    )

    return "OK", 201


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    # Instantiate db session and some repository objects =====
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    # pass the commands into the domain service (use-case) ====
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            repo, session     
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201