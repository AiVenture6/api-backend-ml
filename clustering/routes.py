from flask import Blueprint, request
from clustering.controller import recommend_image

bp = Blueprint('clustering_routes', __name__)


@bp.route("/recommendation/images", methods=["GET"])
def recommended_image_route():
    input_image = request.args.get("local")
    if not input_image:
        return {
            "status": "Error",
            "message": "Parameter 'input_image' is required."
        }, 400

    return recommend_image(input_image)
