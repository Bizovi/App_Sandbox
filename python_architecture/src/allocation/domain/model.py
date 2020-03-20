"""The domain logic, with ValueObjects, Entities and Domain Services.

One typically has more than one module, with base classes for Entity, ValueObjects
Aggregates and (sometimes?) - workflows. As a rule of thumb, domain models should 
have only the data needed to performcalculations.

Choosing Aggregates heavily depends on the bounded context. This way we:
* Keep the number of aggregates llow
* Keep their size manageable
* One aggregate should have one repository
* Aggregates are the only entities accessible to external world
"""

from typing import List, Dict, Tuple, Set, Optional, NewType
from dataclasses import dataclass
from datetime import date

from allocation.domain import events

# =========== Define types + Exceptions ===============
# =====================================================
Quantity = NewType("Quantity", int)

Sku = NewType("Sku", str)
BatchReference = NewType("BatchReference", str)
OrderReference = NewType("OrderReference", str)

class OutOfStock(Exception):
    pass

# =========== Value objects (without identity) ========
# =====================================================
@dataclass(unsafe_hash=True)
class OrderLine:
    """Alternative is to use `pydantic` as an abstraction over dataclasses

    Some remarks:   
    * Dataclasses automatically check for structural equality!
    * If we change any of the values -> we get a new OrderLine. 
    * We get .__hash__() for free because of immutability

    On ORM usage:
    * `frozen=True` will not work with SQLAlchemy
    * need `unsafe_hash=True`, which is a **shady hack**
    """
    orderid: OrderReference
    sku: Sku
    qty: Quantity


# =========== Entities with behavior ==================
# =====================================================
class Batch(object):
    """Is an entify, has a lifecycle and behavior. Notice how OrderLine 
    is passed into allocate method.
    
    The model can be more realistic to take into account:
        * delivery on specific future dates -> choose batch to allocate
        * some skus aren't in batches -> ordered on demand
        * depending on location, can allocate a subset given a warehouse
        * choose the region from which to ship

    Another controversial topic is **mutation:** would prefer everything to be
    immutable, but then there is no point in OOP besides namespacing
    """
    def __init__(self, 
        ref: BatchReference, sku: Sku, qty: Quantity, eta: Optional[date]
    ) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta

        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def __repr__(self) -> str:
        """Display the representation of the object (entity -> id)"""
        return f'<Batch {self.reference}>'

    def __eq__(self, other) -> bool:
        """Override the equality for comparing the entities by ids."""
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        """If we want to use objects in sets or as keys of a dictionary."""
        return hash(self.reference)

    def __gt__(self, other) -> bool:
        """Important for `sortable`, knowing how to sort an array of batches"""
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine) -> None:
        """Would be perfect if would return a new object and not mutate"""
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)
    
    @property
    def allocated_quantity(self) -> int:
        """Calculated property based on the state"""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        """A helper function which checks if can allocate SKU to a batch.
        Checks if line (SKU) exists in batch and that there is enough inventory.
        """
        return self.sku == line.sku and self.available_quantity >= line.qty


# =========== Domain Service Functions ================
# =====================================================
def allocate(line: OrderLine, batches: List[Batch]) -> BatchReference:
    """A domain service which allocates SKUs to a batch and returns batch refs.
    
    The functional equivalent of this would be much neater, especially with a 
    `map fn xs` (e.g. from toolz). It would also avoid interrupting exec flow.

    DEPRECATED - Since we have it in the Product aggregate
    """
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)  # mutation here :(
        return batch.reference
    except StopIteration:
        # can't find it in any of the batches
        raise OutOfStock(f'Out of stock for sku {line.sku}')


# =========== Aggregates and Data Consistency ================
# ============================================================
class Product:  # GlobalSKUStock
    """Could be also called GlobalSkuStock. It is an aggregate/cluster of entities"""
    
    def __init__(self, sku: Sku, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

        self.events: List[events.Event] = []

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            self.events.append(events.OutOfStock(line.sku))

            # the event now does the job of the exception
            # raise OutOfStock(f"Out of stock for sku {line.sku}")
