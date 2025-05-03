import asyncio
from database import SessionLocal
from models import Order, Shipment

async def insert_sample_data():
    async with SessionLocal() as session:
        order1 = Order(id=1, customer="Alice")
        order2 = Order(id=2, customer="Bob")
        order3 = Order(id=3, customer="Charlie")

        shipments = [
            Shipment(order_id=1), Shipment(order_id=1),
            Shipment(order_id=2)
        ]

        session.add_all([order1, order2, order3] + shipments)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(insert_sample_data())