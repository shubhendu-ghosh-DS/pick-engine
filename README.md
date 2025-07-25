
# PickEngine - Recommendation API Backend for SmartPick

**PickEngine** is a scalable, modular **FastAPI**-based backend system powering the SmartPick UI. It provides intelligent product recommendations for electronic appliances using a combination of KNN-based ML models, MongoDB storage, and dynamic query filtering.

---

## 🧠 Core Features

- 🔌 **REST API Endpoints** to serve appliances, filter products, and fetch recommendations.
- 🧾 **Fast MongoDB Queries** with optional filtering and pagination.
- 🤖 **Appliance-Specific ML Models** using pre-trained KNN algorithms.
- ⚙️ **Preprocessing Pipelines** with label encoders for categorical data.
- 🔄 **ID-safe JSON Serialization** using BSON-to-JSON conversion utilities.
- 🚀 **Ready for Docker, Hugging Face Spaces, or Cloud Deployment.**

---

## 🗂️ Project Structure

```
pickengine/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── db.py                  # MongoDB connection setup
│   └── utils.py               # Recommendation logic, preprocessing
├── models/                    # Pre-trained models, encoders, features (loaded at startup)
│   ├── ac_knn_model.pkl
│   ├── ac_encoders.pkl
│   ├── ac_features.pkl
│   └── ...
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ API Endpoints

### 1. `GET /appliances`
Returns the list of available appliances with their names and image URLs.

**Response:**
```json
[
  { "name": "TV", "image": "https://..." },
  { "name": "AC", "image": "https://..." }
]
```

---

### 2. `GET /products/`
Returns a paginated, optionally filtered, and sorted list of products for a given appliance.

**Query Parameters:**
- `appliance`: Required. One of `tv`, `ac`, `fridge`, `wash`
- `brand`: (optional) filter by brand
- `sort`: (optional) `asc` or `desc` for price sorting
- `page`: (default `1`)
- `limit`: (default `10`)

**Example:**
```
GET /products/?appliance=tv&brand=LG&sort=asc&page=2
```

---

### 3. `GET /recommend/{appliance}/{product_id}`
Returns the full product details and a list of recommended alternatives.

**Example:**
```
GET /recommend/tv/66a1c3a932823b67bd492f10
```

**Response:**
```json
{
  "product": { ... }, 
  "recommendations": [
    { "name": "Sony Bravia", "ratings": 4.5, ... },
    ...
  ]
}
```

---

## 🧠 Machine Learning Logic

Recommendations are powered by **KNN models**, trained individually for each appliance category (`tv`, `ac`, `fridge`, `wash`).

### How It Works:
- When a product is requested for recommendation:
  - It's **preprocessed** (label-encoded + normalized)
  - Transformed into a **feature vector**
  - Fed to the appliance-specific **KNN model**
  - Returns top 5 most similar products from the training set
- Label encoders handle unseen values gracefully using safe defaults.

---

## 🧪 Preprocessing & Encoding

Each appliance has:
- `.pkl` model file (KNN)
- `.pkl` label encoders (dictionary of encoders)
- `.pkl` feature set (used for KNN search)

**Dynamic feature mapping** by appliance:

| Appliance | Features Used |
|----------|----------------|
| TV       | ratings, actual_price, brand, length, LED, smart, ultra_hd |
| AC       | ratings, actual_price, brand, power, star, inverter |
| Fridge   | ratings, actual_price, brand, capacity, energy_star, door, cooling_tech |
| Washing  | ratings, actual_price, brand, weight, load, energy_star |

---

## 🧬 Environment Variables

**MongoDB URI** must be set in the environment:

```env
MONGO_URI=mongodb+srv://<user>:<pass>@cluster0.mongodb.net
```

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shubhendu-ghosh-DS/pick-engine.git
cd pickengine
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Start the Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 7861 --reload
```

---

## 📦 Docker Deployment (Hugging Face or Custom)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7861
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7861"]
```

---

## 🧾 Requirements

```
fastapi
pydantic
pymongo
scikit-learn
uvicorn
joblib
pandas
```

---

## ✅ Example Use Case

When a user selects a product in the SmartPick UI:
- `/recommend/{appliance}/{product_id}` is triggered
- The backend:
  1. Retrieves the full product details from MongoDB
  2. Preprocesses it for ML
  3. Queries KNN model
  4. Returns 5 most similar products

---

## 👨‍💻 Author

**Shubhendu Ghosh**  
🔗 [GitHub](https://github.com/shubhendu-ghosh-DS)  
📧 [Email](mailto:shubhendughosh00@gmail.com)

---

## 📄 License

This project is licensed under the MIT License.

---
```

