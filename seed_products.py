from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Connect to the SAME database that is currently working
DATABASE_URL = "postgresql://postgres:09012004Adi@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the model locally just for this script to avoid import errors
class Product(Base):
    __tablename__ = "products"
    productID = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    availabilityStatus = Column(Integer)

def seed():
    db = SessionLocal()
    # Check if we already have products to avoid duplicates
    existing = db.query(Product).count()
    if existing > 0:
        print(f"Inventory already has {existing} items. Skipping seed.")
        return

    sample_products = [
        Product(name="Industrial Turbine", price=12500.00, availabilityStatus=45),
        Product(name="Hydraulic Pump", price=850.50, availabilityStatus=12),
        Product(name="Solar Inverter", price=2100.00, availabilityStatus=80),
        Product(name="Steel Girders (Batch)", price=5400.00, availabilityStatus=5),
        Product(name="Copper Wiring Reel", price=320.00, availabilityStatus=150)
    ]
    
    db.add_all(sample_products)
    db.commit()
    print("Successfully added 5 SKUs to your Live Inventory!")
    db.close()

if __name__ == "__main__":
    seed()
