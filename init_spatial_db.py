import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base
import models  # Important: This registers your Station and Route models

# Using the correct async engine creator and your Docker password
ASYNC_URL = "postgresql+asyncpg://postgres:09012004Adi@localhost:5432/postgres"

async def init_models():
    engine = create_async_engine(ASYNC_URL)
    async with engine.begin() as conn:
        print("Connecting to database and creating tables...")
        # This creates stations, train_routes, and delivery_performance
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully in the PostGIS container!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())
