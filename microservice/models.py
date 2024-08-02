from sqlalchemy import Column, Integer, String, UniqueConstraint

from db import Base, metadata


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(200))
    image_url = Column(String(200))
    likes = Column(Integer, default=0)


class ProductUser(Base):
    __tablename__ = 'product_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )
