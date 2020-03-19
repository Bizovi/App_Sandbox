from typing import List, Dict, Tuple, Set, Optional, NewType
from dataclasses import dataclass

from datetime import date

# =========== Define types + Exceptions ===============
# =====================================================
Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)

BatchReference = NewType("BatchReference", str)
OrderReference = NewType("OrderReference", str)
ProductReference = NewType("ProductReference", str)

class OutOfStock(Exception):
    pass


# =========== Value objects (without identity) ========
# =====================================================
@dataclass(unsafe_hash=True)
class OrderLine:
    """Alternative is to use `pydantic` as an abstraction over dataclasses

    Some remarks:   
    * Dataclasses automatically check for structural equality -> what we need.
    * If we change any of the values -> we get a new OrderLine. 
    * We get .__hash__() for free because of immutability

    On ORM usage
    * `frozen=True` will not work with SQLAlchemy
    * need `unsafe_hash=True`
    """
    orderid: OrderReference
    sku: ProductReference
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

        # understanding which lines have been allocated
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()
    
    def allocate(self, line: OrderLine) -> None:
        """Would be perfect if would return a new object and not mutate"""
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    
    @property
    def allocated_quantity(self) -> int:
        """Calculated property based on the state"""
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def __eq__(self, other):
        """Override the equality for checking the entity. Can also override
        the .__hash__() for usage in sets and as dict keys
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other) -> bool:
        """Syntactic sugar to know which ETA is greater"""
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __repr__(self) -> str:
        return f'<Batch {self.reference}>'


# =========== Domain Service Functions ================
# =====================================================
def allocate(line: OrderLine, batches: List[Batch]) -> BatchReference:
    """The functional equivalent of this would be much neater, especially
    with a `map fn xs` (e.g. from toolz). It would also avoid interrupting
    the execution flow.
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
