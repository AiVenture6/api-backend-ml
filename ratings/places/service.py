import pandas as pd
from config import model_svd, df_tourism_with_id, df_tourism_rating, df_merged


def rekomendasi_pengguna_baru(kategori, lokasi=None, top_n=5):
    """
    Rekomendasi tempat wisata untuk pengguna baru berdasarkan kategori wisata dan lokasi.
    """
    # Filter berdasarkan kategori
    filtered_places = df_merged[df_merged['Category'].str.contains(kategori, case=False)]

    # Filter berdasarkan lokasi jika disediakan
    if lokasi:
        filtered_places = filtered_places[filtered_places['City'].str.contains(lokasi, case=False)]

    # Urutkan berdasarkan rating rata-rata tempat wisata
    rekomendasi = (
        filtered_places[['Place_Name', 'Category', 'City', 'Rating']]
        .drop_duplicates()
        .sort_values(by='Rating', ascending=False)
        .head(top_n)
    )
    return rekomendasi

def rekomendasi_pengguna_lama(user_id, top_n=5):
    """
    Memberikan rekomendasi untuk pengguna lama berdasarkan model SVD yang telah dilatih dan interaksi pengguna lain yang serupa.
    """
    # Ambil semua Place_Id
    all_places = df_tourism_rating['Place_Id'].unique()

    # Tempat yang sudah pernah dilihat oleh user
    seen_places = df_tourism_rating[df_tourism_rating['User_Id'] == user_id]['Place_Id'].unique()

    # Prediksi rating untuk tempat yang belum dilihat
    rekomendasi = []
    for place_id in all_places:
        if place_id not in seen_places:
            pred = model_svd.predict(user_id, place_id)
            rekomendasi.append((place_id, pred.est))

    # Urutkan berdasarkan rating prediksi tertinggi
    rekomendasi = sorted(rekomendasi, key=lambda x: x[1], reverse=True)[:top_n]

    # Ambil detail tempat wisata yang direkomendasikan
    rekomendasi_df = pd.DataFrame(rekomendasi, columns=['Place_Id', 'Predicted_Rating'])
    rekomendasi_df = rekomendasi_df.merge(df_tourism_with_id[['Place_Id', 'Place_Name', 'Category']], on='Place_Id')

    return rekomendasi_df[['Place_Id', 'Place_Name', 'Category', 'Predicted_Rating']]

