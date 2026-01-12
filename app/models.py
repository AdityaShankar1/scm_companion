from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from .database import Base

class Product(Base):
    __tablename__ = "products"

    # name="columnName" ensures Postgres finds the case-sensitive columns
    # This prevents the 'UndefinedColumnError' you saw earlier
    productID = Column(Integer, primary_key=True, index=True, name="productID")
    name = Column(String, name="name")
    price = Column(Float, name="price")
    availabilityStatus = Column(Integer, default=100, name="availabilityStatus")

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    state = Column(String)
    # PostGIS Geometry column for spatial indexing
    location = Column(Geometry(geometry_type='POINT', srid=4326))

class TrainRoute(Base):
    __tablename__ = "train_routes"
    id = Column(Integer, primary_key=True)
    number = Column(String)
    name = Column(String)
    path = Column(Geometry(geometry_type='LINESTRING', srid=4326))

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    train_number = Column(String)
    train_name = Column(String)
    station_code = Column(String)
    arrival = Column(String)
    departure = Column(String)
    day = Column(Integer)

class DeliveryPerformance(Base):
    __tablename__ = "delivery_performance"
    id = Column(Integer, primary_key=True)
    order_id = Column(String)
    weather = Column(String)
    traffic = Column(String)
    delivery_time = Column(Integer)
    store_loc = Column(Geometry(geometry_type='POINT', srid=4326))
    drop_loc = Column(Geometry(geometry_type='POINT', srid=4326))