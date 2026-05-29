"""Tests for Product Rating API."""
import pytest
from datetime import datetime
from rating import Rating, RatingStore, store


class TestRatingModel:
    """Test Rating data model validation."""

    def test_valid_rating(self):
        """Valid rating creates successfully."""
        rating = Rating(
            product_id="prod-123",
            score=5,
            comment="Great product"
        )
        assert rating.product_id == "prod-123"
        assert rating.score == 5
        assert rating.comment == "Great product"
        assert rating.id
        assert isinstance(rating.created_at, datetime)

    def test_rating_score_boundary_valid(self):
        """Score at boundaries (1, 5) are valid."""
        rating_low = Rating(product_id="prod-1", score=1)
        rating_high = Rating(product_id="prod-2", score=5)
        assert rating_low.score == 1
        assert rating_high.score == 5

    def test_rating_score_too_low(self):
        """Score below 1 raises ValueError."""
        with pytest.raises(ValueError, match="score must be between 1 and 5"):
            Rating(product_id="prod-1", score=0)

    def test_rating_score_too_high(self):
        """Score above 5 raises ValueError."""
        with pytest.raises(ValueError, match="score must be between 1 and 5"):
            Rating(product_id="prod-1", score=6)

    def test_rating_empty_product_id(self):
        """Empty product_id raises ValueError."""
        with pytest.raises(ValueError, match="product_id must be a non-empty string"):
            Rating(product_id="", score=3)

    def test_rating_non_string_product_id(self):
        """Non-string product_id raises ValueError."""
        with pytest.raises(ValueError, match="product_id must be a non-empty string"):
            Rating(product_id=123, score=3)

    def test_rating_non_int_score(self):
        """Non-int score raises ValueError."""
        with pytest.raises(ValueError, match="score must be an integer"):
            Rating(product_id="prod-1", score="3")

    def test_rating_optional_comment(self):
        """Comment is optional, defaults to None."""
        rating = Rating(product_id="prod-1", score=3)
        assert rating.comment is None

    def test_rating_non_string_comment(self):
        """Non-string comment raises ValueError."""
        with pytest.raises(ValueError, match="comment must be a string"):
            Rating(product_id="prod-1", score=3, comment=123)


class TestRatingStore:
    """Test RatingStore operations."""

    def test_save_and_retrieve(self):
        """Can save and retrieve rating."""
        rating = Rating(product_id="prod-1", score=4)
        saved = store.save(rating)
        retrieved = store.get(rating.id)
        assert retrieved.id == rating.id
        assert retrieved.product_id == "prod-1"

    def test_get_nonexistent_returns_none(self):
        """Getting non-existent ID returns None."""
        assert store.get("nonexistent-id") is None

    def test_multiple_ratings(self):
        """Store handles multiple ratings."""
        r1 = Rating(product_id="prod-1", score=5)
        r2 = Rating(product_id="prod-2", score=3)
        store.save(r1)
        store.save(r2)
        assert store.get(r1.id).score == 5
        assert store.get(r2.id).score == 3


class TestAPIEndpoints:
    """Test Flask API endpoints."""

    def test_post_rating_valid(self, client):
        """POST valid rating returns 201 with rating data."""
        response = client.post("/ratings", json={
            "product_id": "prod-123",
            "score": 5,
            "comment": "Amazing!"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["product_id"] == "prod-123"
        assert data["score"] == 5
        assert data["comment"] == "Amazing!"
        assert "id" in data
        assert "created_at" in data

    def test_post_rating_missing_fields(self, client):
        """POST without required fields returns 400."""
        response = client.post("/ratings", json={"product_id": "prod-1"})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_post_rating_invalid_score(self, client):
        """POST with invalid score returns 400."""
        response = client.post("/ratings", json={
            "product_id": "prod-1",
            "score": 10
        })
        assert response.status_code == 400
        data = response.get_json()
        assert "score must be between 1 and 5" in data["error"]

    def test_post_rating_empty_product_id(self, client):
        """POST with empty product_id returns 400."""
        response = client.post("/ratings", json={
            "product_id": "",
            "score": 3
        })
        assert response.status_code == 400

    def test_post_rating_not_json(self, client):
        """POST without JSON body returns 400."""
        response = client.post("/ratings", data="not json")
        assert response.status_code == 400

    def test_get_rating_found(self, client):
        """GET existing rating returns 200."""
        # First create a rating
        post_resp = client.post("/ratings", json={
            "product_id": "prod-1",
            "score": 4
        })
        rating_id = post_resp.get_json()["id"]

        # Then retrieve it
        get_resp = client.get(f"/ratings/{rating_id}")
        assert get_resp.status_code == 200
        data = get_resp.get_json()
        assert data["id"] == rating_id
        assert data["score"] == 4

    def test_get_rating_not_found(self, client):
        """GET non-existent rating returns 404."""
        response = client.get("/ratings/nonexistent-id")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_list_ratings_empty(self, client):
        """GET /ratings returns empty list when no ratings."""
        response = client.get("/ratings")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 0
        assert data["ratings"] == []

    def test_list_ratings_with_data(self, client):
        """GET /ratings returns all ratings."""
        # Create two ratings
        client.post("/ratings", json={"product_id": "prod-1", "score": 5})
        client.post("/ratings", json={"product_id": "prod-2", "score": 3})

        response = client.get("/ratings")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 2
        assert len(data["ratings"]) == 2


@pytest.fixture(autouse=True)
def clear_store():
    """Clear rating store before each test."""
    store._ratings.clear()
    yield


@pytest.fixture
def client():
    """Flask test client."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
