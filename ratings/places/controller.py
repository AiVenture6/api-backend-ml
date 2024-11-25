from ratings.places.service import rekomendasi_pengguna_baru, rekomendasi_pengguna_lama
from config import df_tourism_with_id

def recommend_new_user(kategori, lokasi=None, top_n=5):
    try:
        recommendations = rekomendasi_pengguna_baru(kategori, lokasi, top_n)
        return {
            "status":"success",
            "recommendations": recommendations.to_dict(orient="records")
        }, 200
    except Exception as e:
        return {
            "status":"error",
            "message":str(e)
        }, 400

def recommend_existing_user(user_id, top_n=5):
    try:
        recommendations = rekomendasi_pengguna_lama(user_id, top_n)
        return {
            "status":"success",
            "recommendations": recommendations.to_dict(orient="records")
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 400