
import asyncpg
from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass


class ProductModel(BaseModel):
    id: int
    article: str
    image: str
    stock: int
    store_presence: str
    cost_price: float
    order_quantity: int
    comment: str


@dataclass
class Database:
    pool: Optional[asyncpg.Pool] = None

    async def initialize(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(
                user="",
                password="",  
                database="order_management_dbs",
                host="localhost",
                port=5432,
            )
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

    async def get_product_by_article(self, article: str) -> Optional[ProductModel]:

        if not self.pool:
            return None

        query = """
            SELECT id, article, image, stock, store_presence, 
                   cost_price, order_quantity, comment
            FROM orders_product
            WHERE article = $1
        """
        try:
            async with self.pool.acquire() as conn:
                record = await conn.fetchrow(query, article)
                if record:
                    return ProductModel(**record)
        except Exception as e:
            print(f"Ошибка при запросе к БД: {e}")
        return None
