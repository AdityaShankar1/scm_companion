import json
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Station, TrainRoute, Schedule, DeliveryPerformance, Base

# Absolute Paths
BASE_PATH = "/Users/adityashankar/Downloads"
STATIONS_PATH = os.path.join(BASE_PATH, "archive11/stations.json")
TRAINS_PATH = os.path.join(BASE_PATH, "archive11/trains.json")
SCHEDULES_PATH = os.path.join(BASE_PATH, "archive11/schedules.json")
AMAZON_CSV_PATH = os.path.join(BASE_PATH, "amazon_delivery2.csv")

DATABASE_URL = "postgresql://postgres:09012004Adi@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def ingest():
    # 0. Create all tables first
    Base.metadata.create_all(bind=engine)
    session = Session()
    print("🚀 Starting Ingestion...")

    try:
        # 1. Stations
        if os.path.exists(STATIONS_PATH):
            with open(STATIONS_PATH, 'r') as f:
                data = json.load(f)
                for feat in data['features']:
                    try:
                        if feat['geometry']:
                            lon, lat = feat['geometry']['coordinates']
                            st = Station(
                                code=feat['properties']['code'],
                                name=feat['properties']['name'],
                                state=feat['properties']['state'],
                                location=f"POINT({lon} {lat})"
                            )
                            session.merge(st)
                    except:
                        continue
            session.commit()
            print("✅ Stations Synced")

        # 2. Train Routes (FIXED: Skips invalid 1-point lines)
        if os.path.exists(TRAINS_PATH):
            with open(TRAINS_PATH, 'r') as f:
                data = json.load(f)
                for feat in data['features']:
                    try:
                        coords_list = feat['geometry']['coordinates']
                        if len(coords_list) < 2: continue  # PostGIS needs 2 points for a line

                        coords_str = ", ".join([f"{c[0]} {c[1]}" for c in coords_list])
                        tr = TrainRoute(
                            number=feat['properties'].get('number'),
                            name=feat['properties'].get('name'),
                            path=f"LINESTRING({coords_str})"
                        )
                        session.add(tr)
                    except:
                        continue
            session.commit()
            print("✅ Train Routes Synced")

        # 3. Schedules
        if os.path.exists(SCHEDULES_PATH):
            with open(SCHEDULES_PATH, 'r') as f:
                data = json.load(f)
                for entry in data:
                    try:
                        sch = Schedule(
                            train_number=str(entry.get('train_number')),
                            train_name=entry.get('train_name'),
                            station_code=entry.get('station_code'),
                            arrival=str(entry.get('arrival')),
                            departure=str(entry.get('departure')),
                            day=int(entry.get('day')) if str(entry.get('day')).isdigit() else 0
                        )
                        session.add(sch)
                    except:
                        continue
            session.commit()
            print("✅ Schedules Synced")

        # 4. Amazon Delivery (FIXED: Row-by-row to avoid type errors)
        if os.path.exists(AMAZON_CSV_PATH):
            df = pd.read_csv(AMAZON_CSV_PATH, sep=None, engine='python')
            for _, row in df.iterrows():
                try:
                    dp = DeliveryPerformance(
                        order_id=str(row['Order_ID']),
                        weather=str(row['Weather']).strip(),
                        traffic=str(row['Traffic']).strip(),
                        delivery_time=int(row['Delivery_Time']),
                        store_loc=f"POINT({row['Store_Longitude']} {row['Store_Latitude']})",
                        drop_loc=f"POINT({row['Drop_Longitude']} {row['Drop_Latitude']})"
                    )
                    session.add(dp)
                except:
                    continue
            session.commit()
            print("✅ Amazon Delivery Synced")

        print("\n🎉 SUCCESS: All data is in the database.")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    ingest()