from clustering.service import recommend_images
from config import feature_extractor, features_dict, kmeans, pca

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