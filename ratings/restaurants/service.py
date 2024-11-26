from config import resto, booking_restaurant, scaler_restaurant
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import pandas as pd


# NEW USER
def get_best_resto_by_new(user_id, city=None, top_n=5):
    resto_copy = resto.copy()  # Create a copy of the resto dataset

    if city:
        resto_copy = resto_copy[resto_copy["city"].str.lower() == city.lower()]
    if city:
        resto_copy = resto_copy[resto_copy["city"] == city]
        if resto_copy.empty:
            raise ValueError(f"No hotels found for the city: {city}")

    # Normalize rating, penjualan_3months, and price using the pre-trained scaler
    columns_to_normalize = ['rating', 'penjualan_3months', 'price']
    resto_copy[columns_to_normalize] = scaler_restaurant.transform(resto_copy[columns_to_normalize])

    # Normalize 'jarak' separately using a new scaler
    jarak_scaler = MinMaxScaler()
    resto_copy['jarak'] = jarak_scaler.fit_transform(resto_copy[['jarak']])

    # Invert 'jarak' and 'price' so that lower values are better
    resto_copy['jarak_new'] = 1 - resto_copy['jarak']
    resto_copy['price_new'] = 1 - resto_copy['price']

    # Calculate the overall score using weighted features
    weights = {'rating': 0.2, 'penjualan_3months': 0.1, 'price_new': 0.1, 'jarak_new': 0.6}
    resto_copy['score_new'] = (
            resto_copy['rating'] * weights['rating'] +
            resto_copy['penjualan_3months'] * weights['penjualan_3months'] +
            resto_copy['jarak_new'] * weights['jarak_new'] +
            resto_copy['price_new'] * weights['price_new']
    )

    # Sort the restos based on the new score and return the top N recommendations
    recommended_resto = resto_copy.sort_values(by=['score_new', 'name'], ascending=[False, True]).head(top_n)
    recommended_names = recommended_resto['name'].tolist()  # Extract the recommended resto names

    # Retrieve and return detailed data for the recommended restos
    all_data_for_recommended_resto = resto[resto['name'].isin(recommended_names)]
    all_data_for_recommended_resto = all_data_for_recommended_resto.set_index('name').loc[
        recommended_resto['name']].reset_index()

    return all_data_for_recommended_resto
    # return recommended_resto[['name', 'city', 'score_new', 'jarak_new', 'rating', 'penjualan_3months']]


# OLD USER

def recommend_by_city_and_similarity(user_id, top_n):
    user_booking = booking_restaurant[booking_restaurant['user_id'] == user_id].copy()
    user_booking = user_booking[user_booking['resto_id'].notnull()]
    user_booking = user_booking.sort_values(by='booking_date', ascending=False)

    # Hitung persebaran frekuensi kota favorit berdasarkan resto yang dikunjungi
    city_counts = user_booking.merge(resto, on='resto_id')['city'].value_counts(normalize=True)

    # Ambil data resto yang belum dikunjungi
    visited_resto_ids = user_booking['resto_id'].tolist()
    unseen_resto = resto[~resto['resto_id'].isin(visited_resto_ids)].copy()

    # Normalisasi fitur yang ada menggunakan scaler yang sudah disimpan
    unseen_resto[['rating', 'penjualan_3months', 'price']] = scaler_restaurant.transform(
        unseen_resto[['rating', 'penjualan_3months', 'price']])

    # Normalisasi 'jarak' secara terpisah
    jarak_scaler = MinMaxScaler()
    unseen_resto['jarak'] = jarak_scaler.fit_transform(unseen_resto[['jarak']])

    # Inversi 'jarak' dan 'price' untuk memastikan yang lebih dekat dan lebih murah lebih diprioritaskan
    unseen_resto['jarak'] = 1 - unseen_resto['jarak']  # Jarak lebih dekat mendapat skor lebih tinggi
    unseen_resto['price'] = 1 - unseen_resto['price']  # Harga lebih rendah mendapat skor lebih tinggi

    # Hitung kemiripan berdasarkan cosine similarity untuk fitur numerik
    feature_columns = ['rating', 'penjualan_3months', 'price']
    unseen_features = unseen_resto[feature_columns].values
    seen_resto = resto[resto['resto_id'].isin(visited_resto_ids)].copy()
    seen_resto[feature_columns] = scaler_restaurant.transform(
        seen_resto[feature_columns])  # Transformasi fitur yang terlihat
    seen_features = seen_resto[feature_columns].values
    similarity_scores = cosine_similarity(seen_features, unseen_features)
    unseen_resto['similarity_score'] = similarity_scores.mean(axis=0)

    # Tambahkan skor kota favorit
    unseen_resto['city_rank'] = unseen_resto['city'].apply(lambda city: city_counts.get(city, 0))

    # Tambahkan similarity score berdasarkan deskripsi resto
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_unseen = vectorizer.fit_transform(
        unseen_resto['des'].fillna(''))  # TF-IDF untuk resto yang belum dikunjungi
    with open('tfidf_vectorizer.pkl', 'wb') as file:
        pickle.dump(vectorizer, file)
    tfidf_matrix_seen = vectorizer.transform(seen_resto['des'].fillna(''))  # TF-IDF untuk resto yang sudah dikunjungi

    # Hitung cosine similarity untuk deskripsi
    description_similarity = cosine_similarity(tfidf_matrix_seen, tfidf_matrix_unseen)
    unseen_resto['description_similarity'] = description_similarity.mean(axis=0)

    # Gabungkan similarity score berdasarkan fitur numerik dan deskripsi
    unseen_resto['final_similarity_score'] = (unseen_resto['similarity_score'] + unseen_resto[
        'description_similarity']) / 2

    # Buat rekomendasi per kota sesuai proporsi
    recommendations = []
    for city, proportion in city_counts.items():
        city_restos = unseen_resto[unseen_resto['city'] == city].copy()
        city_count = int(round(proportion * top_n))
        if city_count > 0:
            city_restos = city_restos.sort_values(by=['final_similarity_score', 'rating'], ascending=[False, False])
            recommendations.append(city_restos.head(city_count))

    # Gabungkan rekomendasi dari semua kota
    recommended_resto = pd.concat(recommendations).head(top_n)
    recommended_names = recommended_resto['name'].tolist()  # Ambil nama-nama resto dari recommended_resto
    all_data_for_recommended_resto = resto[resto['name'].isin(recommended_names)]
    all_data_for_recommended_resto = all_data_for_recommended_resto.set_index('name').loc[
        recommended_resto['name']].reset_index()

    return all_data_for_recommended_resto


# PENGGABUNGAN FUNGSI

def combined_recommendation(user_id, top_n):
    # Cek apakah pengguna memiliki booking
    recent_resto = booking_restaurant[booking_restaurant['user_id'] == user_id].copy()
    # recent_resto = get_recent_resto(booking, user_id, top_n)

    # Jika tidak ada riwayat, gunakan rekomendasi berdasarkan kategori
    if recent_resto.empty:
        # print("Tidak ada booking untuk user ini. Menggunakan rekomendasi berdasarkan kategori.")
        recommended_resto = get_best_resto_by_new(user_id, top_n)
    else:
        # Jika ada booking, gunakan rekomendasi berdasarkan deskripsi
        # print("Booking ditemukan. Menggunakan rekomendasi berdasarkan kemiripan deskripsi.")
        recommended_resto = recommend_by_city_and_similarity(user_id, top_n)

    return recommended_resto
