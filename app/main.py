import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Internal imports - using relative dots for the new app/ folder structure
from . import models
from . import ml_engine
from .database import engine, get_db

# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("scm_companion")

load_dotenv()

# 2. Initialize App
app = FastAPI(title="SCM Companion")

# 3. Mount Static Files & Templates
# Points to app/static and app/templates since we run from the root
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

ADMIN_USER = os.getenv("SCM_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("SCM_ADMIN_PASSWORD", "password123")


def is_authenticated(request: Request):
    return request.cookies.get("scm_session") == "authenticated_user"


@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    async with AsyncSession(engine) as db:
        try:
            result = await db.execute(select(models.Product))
            if not result.scalars().all():
                logger.info("No products found. Seeding default SKUs...")
                sample_products = [
                    models.Product(name="Industrial Turbine", price=12500.0, availabilityStatus=45),
                    models.Product(name="Hydraulic Pump", price=850.5, availabilityStatus=12),
                    models.Product(name="Solar Inverter", price=2100.0, availabilityStatus=80)
                ]
                db.add_all(sample_products)
                await db.commit()
                logger.info("Database seeding complete.")
        except Exception as e:
            logger.error(f"Startup Database Error: {e}")


# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    try:
        result = await db.execute(select(models.Product))
        products = result.scalars().all()
        return templates.TemplateResponse(request, "dashboard.html", {"products": products})
    except Exception as e:
        logger.error(f"Dashboard Load Error: {e}")
        return templates.TemplateResponse(request, "dashboard.html", {"products": [], "error": str(e)})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        logger.info(f"Successful login for user: {username}")
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="scm_session", value="authenticated_user", httponly=True)
        return response
    logger.warning(f"Failed login attempt for user: {username}")
    return RedirectResponse(url="/login?error=1", status_code=303)


@app.get("/logout")
async def logout():
    logger.info("User logged out.")
    response = RedirectResponse(url="/login")
    response.delete_cookie("scm_session")
    return response


@app.get("/forecast/{product_id}")
async def get_forecast(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return {"error": "Unauthorized"}

    result = await db.execute(select(models.Product).where(models.Product.productID == product_id))
    product = result.scalar_one_or_none()

    if not product:
        logger.warning(f"Forecast requested for missing product ID: {product_id}")
        return {"error": "Not found"}

    days_left = ml_engine.predict_days_left(product.availabilityStatus or 100, [5, 10, 8, 12, 15])
    return {"predicted_days_remaining": days_left}


@app.get("/optimize-logistics/{product_id}")
async def optimize_logistics(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return {"error": "Unauthorized"}
    try:
        user_lon, user_lat = 77.2090, 28.6139
        user_point = f'SRID=4326;POINT({user_lon} {user_lat})'
        query = select(models.Station,
                       func.ST_Distance(models.Station.location, func.ST_GeomFromText(user_point)).label(
                           "distance")).order_by("distance").limit(1)

        result = await db.execute(query)
        row = result.first()
        station, distance = row
        logger.info(f"Logistics optimized for product {product_id}. Nearest hub: {station.name}")
        return {"name": station.name, "distance": round(distance * 111, 2), "code": station.code}
    except Exception as e:
        logger.error(f"Logistics Optimization Error: {e}")
        return {"name": "Error", "distance": 0, "error": str(e)}


@app.post("/add_product")
async def add_product(request: Request, name: str = Form(...), price: float = Form(...),
                      db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return RedirectResponse(url="/login")
    try:
        new_prod = models.Product(name=name, price=price, availabilityStatus=100)
        db.add(new_prod)
        await db.commit()
        logger.info(f"New product added: {name}")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        logger.error(f"Add Product Error: {e}")
        return RedirectResponse(url="/", status_code=303)


# --- ADDED ROUTES ---

@app.delete("/delete_product/{product_id}")
async def delete_product(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return {"error": "Unauthorized"}
    try:
        result = await db.execute(select(models.Product).where(models.Product.productID == product_id))
        product = result.scalar_one_or_none()

        if product:
            await db.delete(product)
            await db.commit()
            logger.info(f"Product ID {product_id} deleted successfully.")
            return {"success": True}

        return {"error": "Product not found"}
    except Exception as e:
        logger.error(f"Delete Product Error: {e}")
        return {"error": str(e)}


@app.put("/update_price/{product_id}")
async def update_price(product_id: int, request: Request, price: float = Form(...), db: AsyncSession = Depends(get_db)):
    if not is_authenticated(request):
        return {"error": "Unauthorized"}
    try:
        result = await db.execute(select(models.Product).where(models.Product.productID == product_id))
        product = result.scalar_one_or_none()

        if product:
            product.price = price
            await db.commit()
            logger.info(f"Price updated for Product ID {product_id} to {price}")
            return {"success": True}

        return {"error": "Product not found"}
    except Exception as e:
        logger.error(f"Update Price Error: {e}")
        return {"error": str(e)}