import pickle
import pandas as pd
from sklearn.preprocessing import minmax_scale

with open("https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/Kmeans_model.pkl", "rb") as f:
    kmeans = pickle.load(f)

with open("https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/VGG16_model.pkl", "rb") as f:
    feature_extractor = pickle.load(f)

with open("https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/PCA_model.pkl", "rb") as f:
    pca = pickle.load(f)

with open("https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/tourism_features.pkl", "rb") as f:
    features_dict = pickle.load(f)

with open('https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/svd_model.pkl', 'rb') as f:
    model_svd = pickle.load(f)

with open('https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/scaler_model_hotel.pkl', 'rb') as f:
    scaler_hotel = pickle.load(f)

with open('https://storage.googleapis.com/aiventure_model_ml/machine%20learning%20model/scaler_model_restaurant.pkl', 'rb') as f:
    scaler_restaurant = pickle.load(f)


df_tourism_with_id = pd.read_csv('https://storage.googleapis.com/aiventure_model_ml/dataset/tourism_with_id.csv')  # Path ke tourism_with_id
df_tourism_rating = pd.read_csv('https://storage.googleapis.com/aiventure_model_ml/dataset/tourism_rating.csv')    # Path ke tourism_rating
df_merged = pd.merge(df_tourism_rating, df_tourism_with_id, on='Place_Id', how='inner')
df_merged['Timestamp'] = pd.date_range(start='2023-01-01', periods=len(df_merged), freq='D')

hotel = pd.read_csv('https://storage.googleapis.com/aiventure_model_ml/dataset/Hotel%20DATASET.csv')
booking_hotel = pd.read_csv('https://storage.googleapis.com/aiventure_model_ml/dataset/Booking_hotel.csv')

resto = pd.read_csv("https://storage.googleapis.com/aiventure_model_ml/dataset/Resto%20DATASET.csv")
booking_restaurant = pd.read_csv("https://storage.googleapis.com/aiventure_model_ml/dataset/Booking_restaurant.csv")
