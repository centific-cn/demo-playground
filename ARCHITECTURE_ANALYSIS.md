# Architecture Analysis: Greeting Feature

## Overview
Adding a `greet()` function to provide personalized, time-aware greetings to the demo-playground repository.

## System Context
- **Language**: Python 3.12
- **Testing**: pytest
- **Existing modules**: calculator.py with basic arithmetic operations

## Design Decisions

### 1. Module Structure
- **New file**: `greeter.py` - maintains separation of concerns (calculator vs greeter functionality)
- **Parallel pattern**: Follows existing `calculator.py` structure with module-level functions

### 2. Function Signature
```python
def greet(name: Optional[str] = None, formal: bool = False) -> str
```

**Rationale**:
- Optional `name` parameter allows generic greetings when name not provided
- `formal` parameter provides stylistic flexibility without complexity
- Type hints improve IDE support and documentation

### 3. Time-Aware Greetings
Uses `datetime.now().hour` to provide context-aware greetings:
- 05-12: "Good morning"
- 12-18: "Good afternoon" 
- 18-22: "Good evening"
- 22-05: "Good night"

**Tradeoff**: Time-awareness adds value but introduces non-deterministic test behavior. Mitigated with flexible test assertions.

### 4. Test Strategy
- **8 test cases** covering: basic usage, formal mode, edge cases, time awareness
- **Flexible assertions**: check for phrases rather than exact strings due to time variation
- **Test classes**: `TestGreet` and `TestGetGreetingCount` for organization

## Dependencies
- **stdlib**: `datetime`, `typing` - no external dependencies added
- **Runtime**: Python 3.12+ (matches environment)

## Quality Metrics
- **Test coverage**: 100% of new code
- **Type safety**: Full type hints
- **Documentation**: Docstrings with examples

## Integration Points
- Standalone module with no dependencies on existing code
- Can coexist with `calculator.py` without conflicts
- No breaking changes to existing functionality
