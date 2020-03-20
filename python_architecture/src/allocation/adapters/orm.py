"""Dependency inversion with a popular ORM - SQLAlchemy. Can be easily switched.

The ORM depends the model, but not the other way around! We get the benefits of 
using SQLAlchemy (e.g. alembic for migrations), transparently query domain obj..
"""

from sqlalchemy import (Table, MetaData, Column, Integer, String, Date, ForeignKey)
from sqlalchemy.orm import mapper, relationship

from allocation.domain import model


metadata = MetaData()

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

batches = Table(
    'batches', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta', Date, nullable=True),
)

allocations = Table(
    'allocations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('orderline_id', ForeignKey('order_lines.id')),
    Column('batch_id', ForeignKey('batches.id')),
)


def start_mappers() -> None:
    """Function to load and save domain model instances from and to a database.
    
    If we don't call the function, the model will be unaware of the database.
    Map model.Batch -> Table.batches. We're basically working with an aggregate.
    """
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(model.Batch, batches, properties={
        '_allocations': relationship(
            lines_mapper,
            secondary=allocations,
            collection_class=set,
        )
    })