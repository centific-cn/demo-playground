"""Product Rating API - Flask application."""
from flask import Flask, request, jsonify
from rating import Rating, store

app = Flask(__name__)


@app.post("/ratings")
def create_rating():
    """Create a new product rating."""
    try:
        data = request.get_json(force=False, silent=True)
        if data is None:
            return jsonify({"error": "Request body must be valid JSON"}), 400

        product_id = data.get("product_id")
        score = data.get("score")
        comment = data.get("comment")

        if product_id is None or score is None:
            return jsonify({"error": "product_id and score are required"}), 400

        rating = Rating(
            product_id=product_id,
            score=score,
            comment=comment
        )
        store.save(rating)

        return jsonify({
            "id": rating.id,
            "product_id": rating.product_id,
            "score": rating.score,
            "comment": rating.comment,
            "created_at": rating.created_at.isoformat()
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.get("/ratings/<rating_id>")
def get_rating(rating_id: str):
    """Retrieve a rating by ID."""
    rating = store.get(rating_id)
    if rating is None:
        return jsonify({"error": "Rating not found"}), 404

    return jsonify({
        "id": rating.id,
        "product_id": rating.product_id,
        "score": rating.score,
        "comment": rating.comment,
        "created_at": rating.created_at.isoformat()
    }), 200


@app.get("/ratings")
def list_ratings():
    """List all ratings."""
    ratings = list(store._ratings.values())
    return jsonify({
        "count": len(ratings),
        "ratings": [
            {
                "id": r.id,
                "product_id": r.product_id,
                "score": r.score,
                "comment": r.comment,
                "created_at": r.created_at.isoformat()
            }
            for r in ratings
        ]
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
