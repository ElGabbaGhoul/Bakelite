import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from fastapi import FastAPI, HTTPException

app = FastAPI()

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

employee_ref = db.collection("employees")
item_ref = db.collection("items")

class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class Item:
    def __init__(self, name, quantity, type_of_item):
        self.name = name
        self.quantity = quantity
        self.type_of_item = type_of_item

@app.post("/employee")
async def create_employee(name: str, role: str):
    if role not in ["owner", "manager", "baker"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    employee = Employee(name=name, role=role)
    employee_ref.add({"name": employee.name, "role": employee.role})
    return {"name": employee.name, "role": employee.role}

@app.post("/item")
async def create_item(name: str, quantity: int, type_of_item: str):
    if type_of_item not in ["single", "multiple"]:
        raise HTTPException(status_code=400, detail="Invalid item type")
    item = Item(name=name, quantity=quantity, type_of_item=type_of_item)
    item_ref.add({"name": item.name, "quantity": item.quantity, "type_of_item": item.type_of_item})
    return {"name": item.name, "quantity": item.quantity, "type_of_item": item.type_of_item}

@app.get("/employee")
async def read_employees():
    employees = []
    docs = employee_ref.stream()
    for doc in docs:
        employees.append(doc.to_dict())
    return employees

@app.get("/item")
async def read_items():
    items = []
    docs = item_ref.stream()
    for doc in docs:
        items.append(doc.to_dict())
    return items