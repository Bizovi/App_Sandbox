"""An implementation of the repository pattern, to abstract away the DB layer"""

from typing import List, Set
import abc
from allocation.domain import model


class AbstractRepository(abc.ABC):
    """Not really necessary, as we have `duck typing`, which will do the job.
    We can keep the interface really slim for now and iterate fast.
    """
    def __init__(self):
        """For UOW to ask repo which products have been used"""
        self.seen: Set[model.Product] = set()

    def add(self, product: model.Product):
        """Addds products to .seen"""
        self._add(product)
        self.seen.add(product)
    
    def get(self, sku) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.Product) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku: str) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """A concrete implementation of AbstractRepository, using SQLAlchemy"""
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def _add(self, product) -> None:
        self.session.add(product)

    def _get(self, sku) -> str:
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def list(self) -> List[model.Product]:
        return self.session.query(model.Product).all()