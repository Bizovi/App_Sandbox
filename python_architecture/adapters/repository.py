"""An implementation of the repository pattern, to abstract away the DB layer"""

from typing import List
import abc
from domain import model


class AbstractRepository(abc.ABC):
    """Not really necessary, as we have `duck typing`, which will do the job.
    We can keep the interface really slim for now and iterate fast.
    """
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """A concrete implementation of AbstractRepository, using SQLAlchemy"""
    def __init__(self, session) -> None:
        self.session = session

    def add(self, batch) -> None:
        self.session.add(batch)

    def get(self, reference) -> str:
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self) -> List[model.Batch]:
        return self.session.query(model.Batch).all()