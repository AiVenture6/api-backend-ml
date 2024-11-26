from flask import Blueprint, request
from ratings.places.controller import recommend_new_user, recommend_existing_user

bp = Blueprint("ratings_places_routes", __name__)


@bp.route("/ratings/places", methods=["GET"])
def new_user_recommendations():
    kategori = request.args.get("category")
    lokasi = request.args.get("location")
    top_n = int(request.args.get("top", 5))

    if not kategori:
        return {
            "status": "Error",
            "message": "Category required"
        }, 400

    return recommend_new_user(kategori, lokasi, top_n)


@bp.route("/ratings/places/id", methods=["GET"])
def existing_user_recommendations():
    user_id = request.args.get("user")
    if not user_id:
        return {
            "status": "Error",
            "message": "User not found or missing parameter"
        }, 400
    return recommend_existing_user(int(user_id))
