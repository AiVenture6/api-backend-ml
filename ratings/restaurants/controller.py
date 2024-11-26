from ratings.restaurants.service import get_best_resto_by_new, combined_recommendation, recommend_by_city_and_similarity
from flask import request


def recommend_restaurant_user_new(top_n=5, city=None):
    try:
        top_n = int(request.args.get('top', top_n))
        recommendations = get_best_resto_by_new(user_id=None, city=city, top_n=5)
        return {
            'status': 'success',
            'recommendations': recommendations.to_dict(orient='records')
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 400


def recommend_restaurant_existing_user(user_id, top_n=5, city=None):
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


def recommend_restaurant_combined(user_id, top_n=5, city=None):
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