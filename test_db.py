import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        user="dbadmin",
        password="MwUJ2C8ny@MGCnYR",
        host="public-primary-pg-inbangalore-189799-1664910.db.onutho.com",
        port=5432,
        database="LV_NSE"
    )
    print("DB Connected!")
    await conn.close()

asyncio.run(test())
