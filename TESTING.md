# Testing Guide

This project has comprehensive test coverage for all core functionality.

## Running Tests

### Basic Test Run
```bash
pytest tests/
```

### With Coverage Report
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Generate HTML Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in your browser
```

### Run Specific Test File
```bash
pytest tests/test_generator.py -v
```

### Run Specific Test
```bash
pytest tests/test_generator.py::TestLyricGenerator::test_generate_bars_basic -v
```

## Test Coverage

Current coverage: **94.60%** (72 passing tests)

### Coverage Breakdown
- `src/lyrics/generator.py`: 100%
- `src/lyrics/utils.py`: 100%
- `vault_manager.py`: 100%
- `src/personas/vocab_loader.py`: 96.55%
- `src/utils.py`: 95.24%
- `midi_generator.py`: 91.67%
- `generator_core.py`: 85%

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_generator.py        # Lyric generator tests
├── test_generator_core.py   # Core generator tests
├── test_lyrics_utils.py     # Lyrics utility tests
├── test_midi_generator.py   # MIDI generator tests
├── test_personas.py         # Persona loader tests
├── test_utils.py            # Utility function tests
└── test_vault_manager.py    # Vault manager tests
```

## Writing New Tests

Tests use pytest and follow these conventions:

1. Test files start with `test_`
2. Test classes start with `Test`
3. Test functions start with `test_`
4. Use descriptive names that explain what's being tested

Example:
```python
def test_generate_bars_with_high_flex():
    """Test generating bars with high flex level."""
    generator = LyricGenerator()
    result = generator.generate_bars("Neon Alien", "Fashion", flex=10)
    assert isinstance(result, str)
    assert len(result) > 0
```

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ --cov=. --cov-report=xml --cov-report=term

# Check for minimum coverage (90%)
pytest tests/ --cov=. --cov-fail-under=90
```

## Test Dependencies

- pytest >= 8.0.0
- pytest-cov >= 4.1.0  
- pytest-mock >= 3.12.0

Install with:
```bash
pip install -r requirements.txt
```
