from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, func, update

from models import Product

class CrudBase:
    def __init__(self, model):
        self.model = model

    async def get_paginated(
            self,
            session: AsyncSession,
            page: int = 1,
            page_size: int = 2
    ):
        offset = (page - 1) * page_size
        stmt = select(self.model).offset(offset).limit(page_size)
        result = await session.execute(stmt)
        result = [dict(r._mapping)['Article'] for r in result]
        return result

    async def get_count(
            self,
            session: AsyncSession
    ) -> int:
        stmt = select(func.count()).select_from(self.model)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
            self,
            session: AsyncSession,
            create_obj
    ):
        validated_data = jsonable_encoder(create_obj)
        stmt = insert(self.model).values(**validated_data)
        try:
            await session.execute(stmt)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )
        return validated_data

    async def update(
            self,
            session: AsyncSession,
            id: int,
            obj_new: dict
    ):
        stmt = update(self.model).where(self.model.id == id).values(**obj_new)

        response = await session.execute(stmt)
        obj_current = response.scalar_one()

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail=str(e)
            )
        return obj_current

    async def delete(
            self,
            session: AsyncSession,
            id: int
    ):
        stmt = select(self.model).where(self.model.id == id)

        response = await session.execute(stmt)
        obj = response.scalar_one()
        await session.delete(obj)
        await session.commit()
        return obj


product_crud = CrudBase(Product)
