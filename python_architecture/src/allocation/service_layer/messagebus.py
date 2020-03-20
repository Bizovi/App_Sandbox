from typing import List, Dict, Callable, Type, NewType
from allocation.adapters import email
from allocation.domain import events


HandlerType = Dict[Type[events.Event], List[Callable]]

def handle(event: events.Event):
    for handler in HANDLERS.get(type(event)):
        handler(event)
    

def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_email(
        'stock@made.com', f"Out of stock for {event.sku}"
    )

HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification]
}
