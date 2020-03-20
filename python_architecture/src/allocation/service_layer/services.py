"""A layer in which use-cases/orchestration lives. Doesn't change domain logic!

Do not confuse with "domain services", which belongs to the domain model, but is
neither a ValueObject or entity, e.g. a tax calculator, meaning a function
does the job.
"""

from typing import List, Dict, Tuple, Optional, NewType, TYPE_CHECKING
from datetime import date

from allocation.domain import model
from allocation.domain.model import OrderLine
from allocation.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


def is_valid_sku(sku: model.Sku, batches: List[model.Batch]) -> bool:
    """Checks if an SKU is found in any of the batches"""
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date], 
    uow: unit_of_work.AbstractUnitOfWork
) -> None:
    """Add batch to the database (via the repository pattern). Types are basic
    since they come from external world (i.e. the POST request)
    """
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)

        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork
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

    with uow:  # start the context manager
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        
        # can have a try-finally here to send the message
        batchref = product.allocate(line)
        uow.commit()

    return batchref


def reallocate(line: OrderLine, uow: unit_of_work.AbstractUnitOfWork) -> str:
    """Showing that uow can help to reason about code that happens together
    If deallocate fails, don't want to call allocate
    If allocate fails, don't want to commit it!

    DEPRECATED - still uses batches
    """
    with uow:
        batch = uow.batches.get(sku=line.sku)
        if batch is None:
            raise InvalidSku(f"Invalid sku {line.sku}")

        batch.deallocate(line)
        allocate(line)
        uow.commit()


def change_batch_quantity(
    batchref: str, new_qty: int, 
    uow: unit_of_work.AbstractUnitOfWork
):
    """In case that alll the merchandise of a container gets lost
    
    DEPRECATED - Still uses batches
    """
    with uow:
        batch = uow.batches.get(reference=batchref)
        batch.change_purchased_quantity(new_qty)

        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            uow.commit()