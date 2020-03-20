import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from allocation.adapters import repository
from allocation import config


class AbstractUnitOfWork(abc.ABC):
    # access to the batchs repository
    products: repository.AbstractRepository

    def __enter__(self) -> repository.AbstractRepository:
        return self

    def __exit__(self, *args):
        self.rollback()
    
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


# will be overritten in integration tests by SQLite
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    config.get_postgres_uri(), isolation_level="REPEATABLE_READ"  # read about!!
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        """Starts a DB session and instantiate a real repositorys"""
        self.session = self.session_factory()
        self.products = repository.SqlAlchemyRepository(self.session)

        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        return self.session.rollback()