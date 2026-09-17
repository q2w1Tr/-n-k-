import os
from datetime import datetime, timezone
from bson import ObjectId
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
mongo = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = mongo[os.getenv("MONGODB_DB", "fashion_custom_ecommerce")]


def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def sample_product():
    return {
        "slug": "ao-thun-studio",
        "name": "Áo thun Studio",
        "description": "Áo cotton unisex, có thể phối màu và thêm thiết kế riêng.",
        "basePrice": 249000,
        "currency": "VND",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80",
        "variants": [
            {"sku": "TS-BLK-S", "color": "Đen", "hex": "#151515", "size": "S", "stock": 12, "price": 249000},
            {"sku": "TS-BLK-M", "color": "Đen", "hex": "#151515", "size": "M", "stock": 18, "price": 249000},
            {"sku": "TS-WHT-M", "color": "Trắng", "hex": "#f6f4ef", "size": "M", "stock": 20, "price": 249000},
            {"sku": "TS-CRM-L", "color": "Kem", "hex": "#e4d6bd", "size": "L", "stock": 7, "price": 259000},
        ],
        "customization": {"printFee": 35000, "maxTextLength": 24},
    }


@app.get("/")
def index():
    product = db.products.find_one({"slug": "ao-thun-studio"}) or sample_product()
    return render_template("index.html", product=serialize(product))


@app.get("/api/products/<slug>")
def get_product(slug):
    product = db.products.find_one({"slug": slug})
    return jsonify(serialize(product or sample_product()))


@app.get("/api/products/base")
def get_base_products():
    products = list(db.products.find({}, {"_id": 0}))
    return jsonify(serialize(products or [sample_product()]))


@app.post("/api/custom-designs")
def create_design():
    payload = request.get_json(force=True)
    required = ("productSlug", "variantSku", "fabricJson", "previewDataUrl")
    if any(not payload.get(field) for field in required):
        return jsonify({"message": "Thiếu dữ liệu thiết kế."}), 400

    doc = {
        "productSlug": payload["productSlug"],
        "variantSku": payload["variantSku"],
        "fabricJson": payload["fabricJson"],
        "previewDataUrl": payload["previewDataUrl"],
        "highResDataUrl": payload.get("highResDataUrl"),
        "createdAt": datetime.now(timezone.utc),
    }
    result = db.custom_designs.insert_one(doc)
    return jsonify({"id": str(result.inserted_id), "message": "Đã lưu thiết kế"}), 201


@app.post("/api/designs/save")
def save_design_alias():
    return create_design()


@app.post("/api/cart")
def add_to_cart():
    payload = request.get_json(force=True)
    if not payload.get("variantSku"):
        return jsonify({"message": "Hãy chọn biến thể."}), 400
    item = {**payload, "createdAt": datetime.now(timezone.utc)}
    result = db.carts.insert_one(item)
    return jsonify({"id": str(result.inserted_id), "message": "Đã thêm vào giỏ hàng"}), 201


@app.post("/api/orders/create")
def create_order():
    payload = request.get_json(force=True)
    shipping = payload.get("shippingInfo", {})
    items = payload.get("items", [])
    required_shipping = ("fullName", "phone", "address")
    if not items or any(not shipping.get(key) for key in required_shipping):
        return jsonify({"message": "Thiếu thông tin nhận hàng hoặc sản phẩm."}), 400
    total = sum(item.get("unitPrice", 0) * item.get("quantity", 1) for item in items)
    result = db.orders.insert_one({"userId": payload.get("userId"), "items": items,
        "shippingInfo": shipping, "paymentMethod": "COD", "totalPrice": total,
        "status": "new", "createdAt": datetime.now(timezone.utc)})
    return jsonify({"id": str(result.inserted_id), "totalPrice": total, "message": "Đặt hàng thành công"}), 201


@app.get("/api/admin/orders")
def admin_orders():
    return jsonify(serialize(list(db.orders.find().sort("createdAt", -1).limit(100))))


if __name__ == "__main__":
    app.run(debug=True)
