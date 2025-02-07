from fastapi import FastAPI, HTTPException, Path
from typing import List
from models import Store, Item, InventoryItem, Order, OrderItem
from bson import ObjectId

app = FastAPI()

# demo storage in memory
stores = []
items = []
orders = []

@app.post("/stores/", response_model=Store)
def create_store(store: Store):
    stores.append(store)
    return store

@app.get("/stores/", response_model=List[Store])
def get_stores():
    return stores

@app.get("/stores/{store_id}", response_model=Store)
def get_store(store_id: str):
    for store in stores:
        if store.id == store_id:
            return store
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
    store_items = [item for item in items if item.store_id == store_id]
    return store_items

@app.get("/stores/{store_id}/items/{item_id}", response_model=InventoryItem)
def get_item(store_id: str, item_id: str):
    for item in items:
        if item.id == item_id and item.store_id == store_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/stores/{store_id}/orders/", response_model=Order)
def create_order(store_id: str, order: Order):
    for store in stores:
        if store.id == store_id:
            order.store_id = store_id
            orders.append(order)
            return order
    raise HTTPException(status_code=404, detail="Store not found")

@app.get("/stores/{store_id}/orders/", response_model=List[Order])
def get_orders(store_id: str):
    store_orders = [order for order in orders if order.store_id == store_id]
    return store_orders

@app.get("/stores/{store_id}/orders/{order_id}", response_model=Order)
def get_order(store_id: str, order_id: str):
    for order in orders:
        if order.id == order_id and order.store_id == store_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
