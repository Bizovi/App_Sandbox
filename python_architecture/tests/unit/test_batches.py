"""Test allocation of order items to a batch of (incoming) products

We rewrite some of our unit tests on domain as service tests to gain flexibility.
The domain unit tests already did their job to act as docs and guide understanding.
"""

from datetime import date
from allocation.domain import model
import pytest

def test_allocating_to_batch_reduces_available_qty():
    """Describes the behavior we want to see from our system. Classes and 
    variables names' use business jargon, so nontechnical users can read it
    """
    # Setup
    batch = model.Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today)
    line = model.OrderLine("order-ref", "SMALL-TABLE", 2)

    # Exercise
    batch.allocate(line)

    # Validate
    assert batch.available_quantity == 18


def make_batch_and_line(sku, batch_qty, line_qty):
    """A fixture / helper function to create batch and line"""
    return (
        model.Batch("batch-001", sku, batch_qty, eta=date.today()),
        model.OrderLine("order-123", sku, line_qty)
    )


def test_can_allocate_if_available_greater_than_required():
    # Setup
    large_batch, small_line = make_batch_and_line("LAMP", 20, 2)

    # Verify
    assert large_batch.can_allocate(small_line)


def test_can_allocate_if_available_smaller_than_required():
    # Setup
    small_batch, large_line = make_batch_and_line("LAMP", 2, 10)

    # Verify
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    # Setup
    batch, line = make_batch_and_line("LAMP", 2, 2)

    # Verify
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    # Setup
    batch = model.Batch("batch-001", "UNCOMFY-CHAIR", 100, eta=None)

    # Exercise
    different_sku_line = model.OrderLine("order-123", "TOASTER", 10)

    # Verify
    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    """Deallocated unallocated line has no effect. Would be easy to model
    with states as Types (FP Style)"""
    # Setyp
    batch, unallocated_line = make_batch_and_line("DECORATIVE", 20, 2)

    # Exercise
    batch.deallocate(unallocated_line)

    # Verify
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    # Setup
    batch, line = make_batch_and_line("DESK", 20, 2)

    # Exercise
    batch.allocate(line)
    batch.allocate(line)

    # Verify
    assert batch.available_quantity == 18


def test_deallocate_allocated_lines():
    # Setup
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)

    # Exercise
    batch.allocate(line)
    batch.deallocate(line)

    # Verify
    assert batch.available_quantity == 20