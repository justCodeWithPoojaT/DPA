from fastapi import FastAPI, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from models import Order, Shipment

app = FastAPI()

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.get("/orders/with-shipment-counts")
async def get_orders_with_shipment_counts(session: AsyncSession = Depends(get_session)):
    stmt = (
        select(Order.id, Order.customer, func.count(Shipment.id).label("shipment_count"))
        .join(Shipment, Shipment.order_id == Order.id, isouter=True)
        .group_by(Order.id)
    )
    result = await session.execute(stmt)
    orders = result.all()
    return [
        {"order_id": row.id, "customer": row.customer, "shipment_count": row.shipment_count}
        for row in orders
    ]