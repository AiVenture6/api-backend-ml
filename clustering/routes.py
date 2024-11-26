from flask import Blueprint, request, jsonify
from clustering.controller import recommend_image, recommend_image_upload

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


@bp.route("/recommendation/images", methods=["POST"])
def recommended_image_route_upload():
    input_image = request.files.get("file")
    if input_image is None or input_image.filename == "":
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        response = recommend_image_upload(input_image)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "Error"
        }), 400
