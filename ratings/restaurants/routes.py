from flask import Blueprint, request
from ratings.restaurants.controller import recommend_restaurant_user_new, recommend_restaurant_existing_user, recommend_restaurant_combined

bp = Blueprint("ratings_restaurants_route", __name__)


@bp.route("/recommendation/restaurants", methods=["GET"])
def recommend_new_user():
    top_n = request.args.get('top', 5)
    city = request.args.get('city')

    if not city:
        return {
            "status": "Error",
            "message": "City required"
        }, 400

    return recommend_restaurant_user_new(top_n=int(top_n), city=city)


@bp.route("/recommendation/restaurants/id", methods=["GET"])
def recommend_existing_user():
    user_id = request.args.get('user')
    top_n = request.args.get('top', 5)
    city = request.args.get('city')

    if not city:
        return {
            "status": "Error",
            "message": "City required"
        }, 400

    if not user_id:
        return {
            "status": "Error",
            "message": "User ID required"
        }, 400

    return recommend_restaurant_existing_user(user_id=user_id, top_n=top_n, city=city)


@bp.route("/recommendation/restaurants/id/history", methods=["GET"])
def recommend_combined():
    user_id = request.args.get('user')
    top_n = request.args.get('top', 5)
    city = request.args.get('city')

    if not city:
        return {
            "status": "Error",
            "message": "City required"
        }, 400

    if not user_id:
        return {
            "status": "Error",
            "message": "User ID required"
        }, 400

    return recommend_restaurant_combined(user_id=user_id, top_n=top_n, city=city)