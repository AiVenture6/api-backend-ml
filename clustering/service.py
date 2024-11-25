import numpy as np
from keras.src.applications.vgg16 import preprocess_input
from keras.src.utils import load_img, img_to_array

def extract_features(image_path, model):
    try:
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        reshaped_img = img_array.reshape(1, 224, 224, 3)
        img_preprocessed = preprocess_input(reshaped_img)
        features = model.predict(img_preprocessed)
        return features
    except Exception as e:
        print(f"Error extracting features from {image_path}: {e}")
        return None

def recommend_images(input_image, feature_extractor, features_dict, kmeans, pca, n_recommendations=7):
    # Ekstraksi fitur dari gambar input
    input_features = extract_features(input_image, feature_extractor)
    if input_features is None:
        print("Error: Tidak dapat mengekstrak fitur dari gambar input.")
        return [], None

    # Transformasi fitur dengan PCA
    input_features_pca = pca.transform(input_features)

    # Prediksi klaster input
    input_cluster = kmeans.predict(input_features_pca)[0]

    # Ambil gambar yang termasuk dalam klaster input
    cluster_images = [img_path for img_path, cluster in zip(features_dict.keys(), kmeans.labels_) if
                      cluster == input_cluster]

    # Hitung jarak antar fitur gambar dalam klaster untuk rekomendasi
    cluster_features = [features_dict[img].squeeze() for img in cluster_images]
    cluster_features_pca = pca.transform(cluster_features)
    distances = np.linalg.norm(cluster_features_pca - input_features_pca, axis=1)
    recommended_indices = np.argsort(distances)[:n_recommendations]

    # Ambil rekomendasi gambar
    recommendations = [cluster_images[i] for i in recommended_indices]
    return recommendations, input_cluster
