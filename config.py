import pickle
import pandas as pd

with open("model/Kmeans_model.pkl", "rb") as f:
    kmeans = pickle.load(f)

with open("model/VGG16_model.pkl", "rb") as f:
    feature_extractor = pickle.load(f)

with open("model/PCA_model.pkl", "rb") as f:
    pca = pickle.load(f)

with open("model/tourism_features.pkl", "rb") as f:
    features_dict = pickle.load(f)

with open('model/svd_model.pkl', 'rb') as f:
    model_svd = pickle.load(f)

df_tourism_with_id = pd.read_csv('model/tourism_with_id.csv')  # Path ke tourism_with_id
df_tourism_rating = pd.read_csv('model/tourism_rating.csv')    # Path ke tourism_rating
df_merged = pd.merge(df_tourism_rating, df_tourism_with_id, on='Place_Id', how='inner')
df_merged['Timestamp'] = pd.date_range(start='2023-01-01', periods=len(df_merged), freq='D')
