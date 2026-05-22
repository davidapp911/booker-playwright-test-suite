# Booker Playwright Test Suite

![CI](https://github.com/davidapp911/booker-playwright-test-suite/actions/workflows/ci.yml/badge.svg)

UI and API test automation suite for the [Restful Booker Platform](https://automationintesting.online), covering browser automation with Playwright and REST API testing with httpx. Tests run on Chromium and Firefox via GitHub Actions.

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

| Variable | Description | Default |
|---|---|---|
| `BASE_URL` | Target application URL | `https://automationintesting.online` |
| `ADMIN_USERNAME` | Admin panel username | `admin` |
| `ADMIN_PASSWORD` | Admin panel password | `password` |

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

A report is generated at `report.html` after each run. On failure, Playwright saves traces to `test-results/` — open them with:

```bash
playwright show-trace test-results/<trace>.zip
```

## Running with Docker

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) to be running.

```bash
docker-compose up
```

This builds the image, runs the full suite inside the container, and writes `report.html` and `test-results/` back to your local machine.

## CI

GitHub Actions runs the full suite on every push and pull request to `main`, in parallel across Chromium and Firefox. Traces and screenshots are uploaded as artifacts on failure and can be downloaded from the Actions run page.

## Tech Stack

| Layer | Tool |
|---|---|
| Browser automation | Playwright + pytest-playwright |
| Test runner | pytest |
| API client | httpx |
| Schema validation | Pydantic v2 |
| Fake data | Faker |
| Reporting | pytest-html |
| Linting | ruff |
| CI | GitHub Actions |
| Containerisation | Docker + docker-compose |
