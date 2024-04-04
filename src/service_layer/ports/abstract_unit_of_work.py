from abc import ABC

from domain import Batch
from .abstract_repository import AbstractRepository


class AbstractUOW(ABC):

    batches: AbstractRepository[Batch]
