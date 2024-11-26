from flask import request
from ratings.hotels.service import get_best_hotel_by_new, recommend_by_city_and_similarity, combined_recommendation


def recommend_hotel_user_new(top_n=5, city=None):
    try:
        top_n = int(request.args.get('top', top_n))
        recommendations = get_best_hotel_by_new(user_id=None, top_n=top_n, city=city)
        return {
            'status': 'success',
            'recommendations': recommendations.to_dict(orient='records')
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400


def recommend_hotel_existing_user(user_id, top_n=5, city=None):
    try:
        top_n = int(request.args.get('top', top_n))
        recommendations = recommend_by_city_and_similarity(user_id=user_id, top_n=top_n, city=city)
        return {
            'status': 'success',
            'recommendations': recommendations.to_dict(orient='records')
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400


def recommend_hotel_combined(user_id, top_n=5, city=None):
    try:
        user_id = int(user_id)
        top_n = int(request.args.get('top', top_n))
        recommendations = combined_recommendation(user_id=user_id, top_n=top_n, city=city)
        return {
            'status': 'success',
            'recommendations': recommendations.to_dict(orient='records')
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400
