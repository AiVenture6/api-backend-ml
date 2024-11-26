from clustering.service import recommend_images
from config import feature_extractor, features_dict, kmeans, pca
from PIL import Image
from io import BytesIO
import os


def recommend_image(input_image):
    try:
        recommendations, input_cluster = recommend_images(input_image, feature_extractor, features_dict, kmeans, pca)
        input_cluster = int(input_cluster)

        return {
            "status": "Success",
            "cluster": input_cluster,
        }, 200

    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }, 500


def recommend_image_upload(input_image):
    try:
        img = Image.open(input_image.stream)
        img.save('temp_image.jpg')
        recommendations, input_cluster = recommend_images('temp_image.jpg', feature_extractor, features_dict, kmeans,
                                                          pca)

        input_cluster = int(input_cluster)

        return {
            "status": "Success",
            "cluster": input_cluster,
            "recommendations": recommendations,
        }, 200
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }, 500
    finally:
        if os.path.exists('temp_image.jpg'):
            os.remove('temp_image.jpg')
