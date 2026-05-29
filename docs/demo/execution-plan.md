# Product Rating API - Execution Plan

## Objective
Implement RESTful API for product ratings with POST/GET endpoints, validation, and comprehensive test coverage.

## Tech Stack
- **Language**: Python 3.x
- **Framework**: Flask (lightweight, matches project simplicity)
- **Testing**: pytest (existing dependency)
- **Validation**: Custom validators + pydantic (if needed)

## Implementation Plan

### Phase 1: Data Model
- Create `Rating` dataclass with fields:
  - `id`: UUID (unique identifier)
  - `product_id`: str (product being rated)
  - `score`: int (1-5 range)
  - `comment`: Optional[str]
  - `created_at`: datetime

### Phase 2: API Layer
- `POST /ratings`:
  - Accept JSON: `{product_id, score, comment?}`
  - Validate: score in [1,5], product_id non-empty
  - Return 201 with created rating or 400/422 for errors
- `GET /ratings/{id}`:
  - Return 200 with rating or 404 if not found

### Phase 3: Testing
- Unit tests for validation logic
- Integration tests for endpoints
- Coverage target: ≥90%

### Phase 4: Quality Gates
- Run pytest with coverage
- Verify all tests pass
- Check linting (if configured)

## File Structure
```
app.py                 # Flask app with endpoints
rating.py              # Rating model and validation
test_ratings.py       # Test suite
requirements.txt       # Add Flask
```

## Success Criteria
- POST /ratings creates valid rating
- GET /ratings/{id} retrieves by ID
- Validation rejects invalid scores
- All tests pass
- Coverage ≥90%
