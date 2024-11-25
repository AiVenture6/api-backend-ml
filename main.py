from flask import Flask
from clustering import routes as cluster_route
from ratings.places import routes as places_route


app = Flask(__name__)

app.register_blueprint(cluster_route.bp)
app.register_blueprint(places_route.bp)


@app.route("/")
def index():
    return {
        "status": "Success",
        "message": "ML API"
    },200

if __name__ == "__main__":
    app.run(debug=True)