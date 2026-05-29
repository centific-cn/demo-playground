"""Rating model and validation for Product Rating API."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Rating:
    """Product rating data model."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str = ""
    score: int = 0
    comment: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Validate rating fields after initialization."""
        if not self.product_id or not isinstance(self.product_id, str):
            raise ValueError("product_id must be a non-empty string")
        if not isinstance(self.score, int):
            raise ValueError("score must be an integer")
        if self.score < 1 or self.score > 5:
            raise ValueError("score must be between 1 and 5")
        if self.comment is not None and not isinstance(self.comment, str):
            raise ValueError("comment must be a string")


class RatingStore:
    """In-memory store for ratings (demo purposes)."""
    def __init__(self):
        self._ratings = {}

    def save(self, rating: Rating) -> Rating:
        """Store a rating."""
        self._ratings[rating.id] = rating
        return rating

    def get(self, rating_id: str) -> Optional[Rating]:
        """Retrieve a rating by ID."""
        return self._ratings.get(rating_id)


# Global store instance
store = RatingStore()
