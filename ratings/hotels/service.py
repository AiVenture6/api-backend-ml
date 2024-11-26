from config import hotel, booking_hotel, scaler_hotel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def get_best_hotel_by_new(user_id, top_n, city=None):
    hotel_copy = hotel.copy()  # Create a copy of the hotel dataset

    if city:
        hotel_copy = hotel_copy[hotel_copy["city"].str.lower() == city.lower()]
    if city:
        hotel_copy = hotel_copy[hotel_copy["city"] == city]
        if hotel_copy.empty:
            raise ValueError(f"No hotels found for the city: {city}")

    # Normalize rating, penjualan_3months, and price using the pre-trained scaler
    columns_to_normalize = ['rating', 'penjualan_3months', 'price']
    hotel_copy[columns_to_normalize] = scaler_hotel.transform(hotel_copy[columns_to_normalize])

    # Normalize 'jarak' separately using a new scaler
    jarak_scaler = MinMaxScaler()
    hotel_copy['jarak'] = jarak_scaler.fit_transform(hotel_copy[['jarak']])

    # Invert 'jarak' and 'price' so that lower values are better
    hotel_copy['jarak_new'] = 1 - hotel_copy['jarak']
    hotel_copy['price_new'] = 1 - hotel_copy['price']

    # Calculate the overall score using weighted features
    weights = {'rating': 0.25, 'penjualan_3months': 0.25, 'jarak_new': 0.3, 'price_new': 0.2}
    hotel_copy['score_new'] = (
            hotel_copy['rating'] * weights['rating'] +
            hotel_copy['penjualan_3months'] * weights['penjualan_3months'] +
            hotel_copy['jarak_new'] * weights['jarak_new'] +
            hotel_copy['price_new'] * weights['price_new']
    )

    # Sort the hotels based on the new score and return the top N recommendations
    recommended_hotel = hotel_copy.sort_values(by=['score_new', 'name'], ascending=[False, True]).head(top_n)
    recommended_names = recommended_hotel['name'].tolist()  # Extract the recommended hotel names

    # Retrieve and return detailed data for the recommended hotels
    all_data_for_recommended_hotel = hotel[hotel['name'].isin(recommended_names)]
    all_data_for_recommended_hotel = all_data_for_recommended_hotel.set_index('name').loc[
        recommended_hotel['name']].reset_index()

    return all_data_for_recommended_hotel
    # return recommended_hotel[['name', 'city', 'score_new', 'jarak_new', 'rating', 'penjualan_3months']]


# OLD USER

def recommend_by_city_and_similarity(user_id, top_n):
    user_booking = booking_hotel[booking_hotel['user_id'] == user_id].copy()
    user_booking = user_booking[user_booking['hotel_id'].notnull()]
    user_booking = user_booking.sort_values(by='booking_date', ascending=False)

    # Hitung persebaran frekuensi kota favorit berdasarkan booking sebelumnya
    city_counts = user_booking.merge(hotel, on='hotel_id')['city'].value_counts(normalize=True)

    # Ambil data hotel yang belum dikunjungi
    visited_hotel_ids = user_booking['hotel_id'].tolist()
    unseen_hotel = hotel[~hotel['hotel_id'].isin(visited_hotel_ids)].copy()

    # Normalisasi fitur 'rating', 'penjualan_3months', dan 'price' menggunakan scaler yang disimpan
    unseen_hotel[['rating', 'penjualan_3months', 'price']] = scaler_hotel.transform(
        unseen_hotel[['rating', 'penjualan_3months', 'price']])

    # Normalisasi 'jarak' secara terpisah
    jarak_scaler = MinMaxScaler()
    unseen_hotel['jarak'] = jarak_scaler.fit_transform(unseen_hotel[['jarak']])

    # Inversi 'jarak' dan 'price'
    unseen_hotel['jarak'] = 1 - unseen_hotel['jarak']  # Jarak lebih dekat mendapatkan skor lebih tinggi
    unseen_hotel['price'] = 1 - unseen_hotel['price']  # Harga lebih rendah mendapatkan skor lebih tinggi

    # Hitung kemiripan berdasarkan cosine similarity
    unseen_features = unseen_hotel[['rating', 'penjualan_3months', 'price', 'jarak']].values
    seen_hotel = hotel[hotel['hotel_id'].isin(visited_hotel_ids)].copy()
    seen_features = seen_hotel[['rating', 'penjualan_3months', 'price', 'jarak']].values
    similarity_scores = cosine_similarity(seen_features, unseen_features)
    unseen_hotel['similarity_score'] = similarity_scores.mean(axis=0)

    # Tambahkan skor kota favorit
    unseen_hotel['city_rank'] = unseen_hotel['city'].apply(lambda city: city_counts.get(city, 0))

    # Buat rekomendasi per kota sesuai proporsi
    recommendations = []
    for city, proportion in city_counts.items():
        city_hotels = unseen_hotel[unseen_hotel['city'] == city].copy()
        city_count = int(round(proportion * top_n))
        if city_count > 0:
            city_hotels = city_hotels.sort_values(by=['similarity_score', 'rating'], ascending=[False, False])
            recommendations.append(city_hotels.head(city_count))

    # Gabungkan rekomendasi dari semua kota
    recommended_hotel = pd.concat(recommendations).head(top_n)
    recommended_names = recommended_hotel['name'].tolist()
    all_data_for_recommended_hotel = hotel[hotel['name'].isin(recommended_names)]
    all_data_for_recommended_hotel = all_data_for_recommended_hotel.set_index('name').loc[
        recommended_hotel['name']].reset_index()

    return all_data_for_recommended_hotel
    # return recommended_hotel[['name', 'city', 'rating', 'price', 'jarak', 'similarity_score']]


# PENGGABUNGAN FUNGSI

def combined_recommendation(user_id, top_n):
    # Cek apakah pengguna memiliki booking
    recent_hotel = booking_hotel[booking_hotel['user_id'] == user_id].copy()

    # Jika tidak ada riwayat, gunakan rekomendasi berdasarkan kategori
    if recent_hotel.empty:
        print("Tidak ada booking untuk user ini. Menggunakan rekomendasi berdasarkan kategori.")
        recommended_hotel = get_best_hotel_by_new(user_id, top_n)
    else:
        # Jika ada booking, gunakan rekomendasi berdasarkan deskripsi
        print("Booking ditemukan. Menggunakan rekomendasi berdasarkan kemiripan deskripsi.")
        recommended_hotel = recommend_by_city_and_similarity(user_id, top_n)

    return recommended_hotel
