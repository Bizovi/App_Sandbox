"""A layer in which use-cases/orchestration lives. Doesn't change domain logic!

Do not confuse with "domain services", which belongs to the domain model, but is
neither a ValueObject or entity, e.g. a tax calculator, meaning a function
does the job.
"""

from typing import List, Dict, Tuple, Optional, NewType
from datetime import date

from allocation.domain import model
from allocation.domain.model import OrderLine
from allocation.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku: model.Sku, batches: List[model.Batch]) -> bool:
    """Checks if an SKU is found in any of the batches"""
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    repo: AbstractRepository, session
) -> None:
    """Add batch to the database (via the repository pattern). Types are basic
    since they come from external world (i.e. the POST request)
    """
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()


def allocate(
    orderid: str, sku: str, qty: int, repo: AbstractRepository, session
) -> str:
    """Services, in general have a very similar series of steps:

    * Fetch something from the repository
    * Make checks or assertions about the request against current state of world
    * Call a domain service
    * If all is well -> save/update any state we changed

    But perfectly, we don't want our service to be **coupled** to DB layer
        -> to be improved with Unit of Work Pattern
    """
    line = OrderLine(orderid, sku, qty)

    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batchref = model.allocate(line, batches)
    session.commit()

    return batchref


def deallocate():
    """TODO(Mihai): """
    pass