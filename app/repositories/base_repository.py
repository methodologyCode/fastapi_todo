import logging
from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(
    filename='example.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(self, data):
        raise NotImplementedError
    
    @abstractmethod
    async def find_one_or_none(self, filter_by):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def add_one(self, data):
        self.logger.debug(f"Adding one record to {self.model.__name__}")
        query = insert(self.model).values(data).returning(self.model)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()
    

    async def delete_one(self, data):
        self.logger.debug(f"Deleting one record to {self.model.__name__}")
        task = await self.find_one_or_none(**data)

        if task is None:
            return None

        query = delete(self.model).filter_by(**data)
        await self.session.execute(query)
        await self.session.commit()
        return task
        
    async def find_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()