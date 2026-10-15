import asyncio
import asyncpg
from config import settings


async def test():
    conn = await asyncpg.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    print("DB Connected!")
    await conn.close()


asyncio.run(test())
