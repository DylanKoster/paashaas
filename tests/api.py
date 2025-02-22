from fastapi import FastAPI, HTTPException, Path
from typing import List
from models import Store, Item, InventoryItem, Order, OrderItem
from bson import ObjectId
from datetime import datetime

app = FastAPI()

# demo storage in memory
stores = []
items = []
orders = []

@app.get("/stores/", response_model=List[Store])
def get_stores():
    return stores

@app.get("/stores/{store_id}", response_model=Store)
def get_store(store_id: str):
    for store in stores:
        if store.id == store_id:
            return store
    raise HTTPException(status_code=404, detail="Store not found")

@app.post("/stores/", response_model=Store)
def create_store(store: Store):
    stores.append(store)
    return store

@app.put("/stores/{store_id}", response_model=Store)
def update_store(store_id: str, store: Store):
    for i, s in enumerate(stores):
        if s.id == store_id:
            stores[i].name = store.name
            stores[i].location = store.location
            return stores[i]
    raise HTTPException(status_code=404, detail="Store not found")

@app.post("/stores/{store_id}/items/", response_model=InventoryItem)
def create_item(store_id: str, item: InventoryItem):
    for store in stores:
        if store.id == store_id:
            item.store_id = store_id
            items.append(item)
            return item
    raise HTTPException(status_code=404, detail="Store not found")

@app.get("/stores/{store_id}/items/", response_model=List[InventoryItem])
def get_items(store_id: str):
    close_expired_orders()
    store_items = [item for item in items if item.store_id == store_id]
    return store_items

@app.get("/stores/{store_id}/items/{item_id}", response_model=InventoryItem)
def get_item(store_id: str, item_id: str):
    close_expired_orders()
    for item in items:
        if item.id == item_id and item.store_id == store_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/stores/{store_id}/items/{item_id}", response_model=InventoryItem)
def update_item(store_id: str, item_id: str, item: InventoryItem):
    close_expired_orders()
    for i, it in enumerate(items):
        if it.id == item_id and it.store_id == store_id:
            items[i].name = item.name
            items[i].img = item.img
            items[i].quantity = item.quantity
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/stores/{store_id}/orders/", response_model=Order)
def create_order(store_id: str, order: Order):
    close_expired_orders()
    for order_item in order.items:
        for item in items:
            if item.id == order_item.item_id:
                if item.quantity < order_item.quantity:
                    raise HTTPException(status_code=400, detail="Not enough stock")
                item.quantity -= order_item.quantity

    for store in stores:
        if store.id == store_id:
            order.store_id = store_id
            orders.append(order)
            return order

    raise HTTPException(status_code=404, detail="Store not found")

@app.get("/stores/{store_id}/orders/", response_model=List[Order])
def get_orders(store_id: str):
    close_expired_orders()
    store_orders = [order for order in orders if order.store_id == store_id]
    return store_orders

@app.get("/stores/{store_id}/orders/{order_id}", response_model=Order)
def get_order(store_id: str, order_id: str):
    close_expired_orders()
    for order in orders:
        if order.id == order_id and order.store_id == store_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/stores/{store_id}/orders/{order_id}", response_model=Order)
def update_order(store_id: str, order_id: str, order: Order):
    close_expired_orders()
    for i, o in enumerate(orders):
        if o.id == order_id and o.store_id == store_id:
            merged_data = {**orders[i].model_dump(), **order.model_dump()}
            merged_data["status"] = order.status
            merged = Order(**merged_data)
            orders[i] = merged
            return orders[i]
    raise HTTPException(status_code=404, detail="Order not found")

def close_expired_orders():
    for order in orders:
        if order.expiry_date < datetime.now():
            order.status = "cancelled"
            for order_item in order.items:
                for item in items:
                    if item.id == order_item.item_id:
                        item.quantity += order_item.quantity

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
