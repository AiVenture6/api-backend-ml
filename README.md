# **ML API Documentation: Ai-venture**

In Collaboration by Cloud Computing and Machine Learning Cohort

## **Overview**

We extend a warm welcome to you, our esteemed reader, to the documentation pertaining to the application programming interface (API). This section contains a comprehensive list of all available endpoints for interacting with the system. Each endpoint is accompanied by a detailed description, a description of the associated method, a list of parameters, and an illustrative sample response. The objective of this documentation is to facilitate the integration of the API into applications by providing guidance to Mobile Development (MD) teams.

---

## **Models and Builtin Dataset**

Required models for this API can be fund or download on this link:

1. [Kmeans_model.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/Kmeans_model.pkl)
2. [PCA_model.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/PCA_model.pkl)
3. [VGG16_model.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/VGG16_model.pkl)
4. [scaler_model_hotel.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/scaler_model_hotel.pkl)
5. [scaler_model_restaurant.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/scaler_model_restaurant.pkl)
6. [svd_model.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/svd_model.pkl)
7. [tfidf_vectorizer.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/tfidf_vectorizer.pkl)
8. [tourism_features.pkl](https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/tourism_features.pkl)

Download models to run locally and make a directory `model` on this clone repository. Ensure the path on each models. on `config.py`

Required builtin dataset for this API can be download on this link:

1. [Booking_hotel.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/Booking_hotel.csv)
2. [Booking_restaurant.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/Booking_restaurant.csv)
3. [Hotel DATASET.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/Hotel%20DATASET.csv)
4. [Resto DATASET.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/Resto%20DATASET.csv)
5. [tourism_with_id.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/tourism_with_id.csv)
6. [tourism_rating.csv](https://storage.googleapis.com/aiventure_model_ml/dataset/tourism_rating.csv)

Download this dataset and make a directory `model` on this clone repository. Ensure the path on each models. on `config.py`

OUR DATA ONLY FOR JAKARTA, BANDUNG, SEMARANG, YOGYAKARTA, AND SURABAYA

---

## **Installation**

Follow the instruction to install API and run locally:
1. `git clone {github repository}`
2. `python -m venv venv`
3. `pip install -r requirements.txt`

---

## **Table of Contents**

1. [Images Recommendations  (`/recommendation/images`)](#images-recommendation)
2. [Destinations Recommendations (`/recommendation/destinations`)](#destinations-recommendation)
3. [Hotels Recommendations (`/recommendation/hotels`)](#hotels-recommendation)
4. [Restaurants Recommendations (`/recommendation/restaurants`)](#restaurants-recommendation)

---

### **1. Images Recommendations  (`/recommendation/images`)**

- **Description:** Endpoint for clustering image to get similar recommendation
- **Available Routes:**
  - `GET /recommendation/images?local={path to image}` (GET)
    - Note: only local image path.
  - `POST /recommendation/images` (POST)
    - Note: image attached.
---

### **2. Destinations Recommendations (`/recommendation/destinations`)**

- **Description:** Endpoint for get destinations recommendation.
- **Available Routes:**
  - `GET /recommendation/destinations?category={category}&location={city}&top=5` (GET)
    - Description: Get 5 destination recommendation by {category} and {location}.
  - `GET /recommendation/destinations/id?user={user_id}` (*)
    - Description: Get destination recommendation based on user_id

---

### **3. Hotels Recommendations (`/recommendation/destinations`)**

- **Description:** Endpoint for get hotels recommendation.
- **Available Routes:**
  - `GET /recommendation/hotels?top=5&city={city}` (GET)
    - Description: Get 5 hotels recommendation by {city}.
  - `GET /recommendation/hotels/id?user={user_id}&top=5&city={city}` (*)
    - Description: Get hotel recommendation based on user_id

---

### **4. Restaurants Recommendations (`/recommendation/destinations`)**

- **Description:** Endpoint for get restaurants recommendation.
- **Available Routes:**
  - `GET /recommendation/restaurants?top=5&city={city}` (GET)
    - Description: Get 5 hotels restaurants by {city}.
  - `GET /recommendation/restaurants/id?user={user_id}&top=5&city={city}` (*)
    - Description: Get hotel restaurants based on user_id

---

