from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from .db import ac_collection, tv_collection, fridge_collection, wash_collection, appliance_collection
from .utils import recommend_product, APPLIANCE_CONFIG, preprocess_single_product
from bson import ObjectId

app = FastAPI()

# Mapping appliance -> db collection
collection_map = {
    "ac": ac_collection,
    "tv": tv_collection,
    "fridge": fridge_collection,
    "wash": wash_collection
}

@app.get("/appliances")
def get_appliances():
    return list(appliance_collection.find({}, {"_id": 0, "name": 1, "image": 1}))

def clean_mongo_data(doc):
    doc["_id"] = str(doc["_id"])
    doc["id"] = str(doc["id"])
    return doc


@app.get("/products/")
def get_products(
    appliance: str,
    brand: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),  # "asc" or "desc"
    page: int = 1,
    limit: int = 10
):
    if appliance not in collection_map:
        raise HTTPException(status_code=404, detail="Appliance not found")

    collection = collection_map[appliance]

    # Build MongoDB query
    query = {}
    if brand:
        query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}

    skip = (page - 1) * limit

    # Build MongoDB cursor
    cursor = collection.find(query)
    if sort in ["asc", "desc"]:
        sort_order = 1 if sort == "asc" else -1
        cursor = cursor.sort("actual_price", sort_order)

    cursor = cursor.skip(skip).limit(limit)

    # Clean ObjectId for JSON serialization
    results = [clean_mongo_data(doc) for doc in cursor]
    return results


@app.get("/recommend/{appliance}/{product_id}")
def recommend(appliance: str, product_id: str):
    if appliance not in collection_map:
        raise HTTPException(status_code=404, detail="Appliance not found")

    collection = collection_map[appliance]
    original_product = collection.find_one({"_id": ObjectId(product_id)})
    if not original_product:
        raise HTTPException(status_code=404, detail="Product not found")
    

    original_product = clean_mongo_data(original_product)

    input_dict = preprocess_single_product(original_product, appliance)

    # Use the new recommend_product function
    try:
        recommendations_df = recommend_product(input_dict, appliance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    print("aLL COOL")

    # Fetch original documents for recommended products using _id
    recommended_ids = recommendations_df['id'].tolist()
    recommended_products = list(collection.find({"id": {"$in": recommended_ids}}))

    # Sanitize documents
    for prod in recommended_products:
        prod['_id'] = str(prod['_id'])  # or use prod.pop('_id', None)

    return {
        "product": original_product,
        "recommendations": recommended_products
    }
