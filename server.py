import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis

# -------- Modèle --------
class Product(BaseModel):
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

# -------- App FastAPI --------
app = FastAPI(title="Store API (Docker + Redis)", version="3.0")

# -------- Connexion Redis --------
# REDIS_HOST = "localhost"
# Pour l'exo 3 en Docker : REDIS_HOST = "redis" (nom du conteneur)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    db=0,
    decode_responses=True
)

def product_key(name: str) -> str:
    return f"product:{name}"

# -------- Endpoints --------

@app.post("/products/", status_code=201)
def create_product(product: Product):
    key = product_key(product.name)
    payload = json.dumps(product.model_dump())
    r.set(key, payload)
    return product

@app.get("/products/{product_name}")
def get_product(product_name: str):
    key = product_key(product_name)
    raw = r.get(key)
    if not raw:
        raise HTTPException(status_code=404, detail="Product not found")
    return json.loads(raw)

@app.get("/products")
def list_products():
    keys = r.keys("product:*")
    items = []
    for k in keys:
        raw = r.get(k)
        if raw:
            items.append(json.loads(raw))
    return items


###########
#############
##############
#################  SAOUDI Selim B2