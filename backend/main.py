from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from datetime import date
import datetime



app = FastAPI(
    title = "Order management",
    description="Order management",
    version="1.0.0"
)


# Order status
class OrderStatus(BaseModel):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"



class Order(BaseModel):
    order_id: str
    customer_name: str
    order_date: date
    total_amount: float
    status: OrderStatus
    
class UpdateStatusRequest(BaseModel):
    status: OrderStatus
     
class OrderSummary(BaseModel):
    total_orders: int
    total_order_value: float
    pending_orders: int
    deliverd_orders: int
    
orders = [
    Order(
        order_id="ORDER001",
        customer_name="Visbin Rojer",
        order_date=date.today(),
        total_amount=1500.50,
        status = OrderStatus.PENDING
    ),
    Order(
            order_id="ORDER002",
            customer_name="john Doe",
            order_date=date.today(),
            total_amount=2500.50,
            status = OrderStatus.PENDING
        ),
    Order(
            order_id="ORDER003",
            customer_name="Vargin Rojer",
            order_date=date.today(),
            total_amount=4500.50,
            status = OrderStatus.PENDING
        ),
    Order(
            order_id="ORDER004",
            customer_name="Visbin Rojer",
            order_date=date.today() + datetime.timedelta(days=1),
            total_amount=1500.50,
            status = OrderStatus.PENDING
        ),
    Order(
            order_id="ORDER005",
            customer_name="John Cena",
            order_date=date.today(),
            total_amount=500.50,
            status = OrderStatus.PENDING
        ),
    
]


@app.get("/")
def home():
    return {
        "message": "Order management home api"
    }
    
@app.get("/orders", response_model=Order)
def get_orders(
    search = Query(
        default=None,
        description="search order by order id or customer name"
                   ),
    status = Query(
        default=None,
        description="filter by ordeer status"
    )
    
):
    result = orders.copy()
    
    if search:
        search_value = search.lower().strip()
        result = [order for order in result if search_value in order.order_id.lower() or search_value in order.customer_name.lower()]
        
    if status:
        result = [order for order in result if order.status == status]
        
    return result


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id):
    for order in orders:
        if order.order_id == order_id:
            return order
        
    raise HTTPException(status_code=404,
                        detail="Order not found")
    
    
    