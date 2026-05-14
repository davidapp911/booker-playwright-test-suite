# Booker Playwright Test Suite

UI and API test automation suite for the Restful Booker Platform using Playwright and pytest.

## Setup

**1. Clone the repo and create a virtual environment**

```bash
git clone <repo-url>
cd booker-playwright-test-suite
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -e .
playwright install
```

**3. Configure environment variables**

Copy the example env file — credentials are already set for this shared learning project:

```bash
cp .env.example .env
```

> The `.env` file is gitignored and must be created manually on each machine. Tests will fail with 401 errors if the file is missing.

## Running Tests

```bash
# All tests
pytest

# UI tests only
pytest tests/ui/

# API tests only
pytest tests/api/

# By marker
pytest -m home
pytest -m booking
pytest -m admin
pytest -m contact
pytest -m auth
```

A report is generated at `report.html` after each run.
