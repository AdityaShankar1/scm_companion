import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Product, Base

DATABASE_URL = "postgresql+asyncpg://postgres:09012004Adi@localhost:5432/scm_db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def populate():
    async with AsyncSessionLocal() as session:
        # Adding items with specific categories for our ML logic
        items = [
            Product(name="Industrial Sensor", category="Critical Electronics", price=450.0),
            Product(name="Steel Rods", category="Raw Materials", price=120.0),
            Product(name="Lube Oil", category="Maintenance", price=85.0)
        ]
        session.add_all(items)
        await session.commit()
        print("Successfully added 3 items to SCM Database!")

if __name__ == "__main__":
    asyncio.run(populate())
