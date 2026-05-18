# CLAUDE.md — booker-playwright-test-suite

## Behavior Instructions

**Never show code unless explicitly asked.** Default to conceptual, descriptive explanations — what to do, why, and how it fits together. Only produce code snippets when the user says something like "show me the code", "write this", "implement this", or similar direct requests.

When helping with this project, prefer:
- Explaining the intent and structure of a solution
- Describing which class, fixture, or file to work in
- Naming the relevant methods or patterns without spelling them out in full
- Pointing to the relevant documentation links listed below

---

## Project Overview

**Project:** booker-playwright-test-suite
**Target:** https://automationintesting.online (Restful Booker Platform)
**Language:** Python 3.12+
**Purpose:** A hands-on learning project covering UI automation with Playwright and API testing with httpx, sharing fixtures and CI infrastructure across both tracks.

The application simulates a hotel-booking site with a public-facing booking flow and a password-protected admin panel. Both the UI and REST API have intentional imperfections, making it a realistic test practice target.

---

## Tech Stack

| Layer | Tool | Notes |
|---|---|---|
| Browser automation | `playwright` + `pytest-playwright` | Replaces Selenium — auto-wait built in |
| Test runner | `pytest` 8.x | Fixtures, parametrize, plugins |
| API client | `httpx` 0.27+ | Sync/async HTTP, cleaner than `requests` |
| Assertions | `expect()` from pytest-playwright | Auto-retrying UI assertions |
| Reporting | `pytest-html` | HTML report with screenshots |
| Linting | `ruff` | Fast lint + format |
| Env config | `python-dotenv` | BASE_URL, credentials from `.env` |
| Fake data | `Faker` | Unique booking payloads per test |
| CI | GitHub Actions | Matrix across Chromium + Firefox |
| Containerisation | Docker + docker-compose | Consistent environment everywhere |
| Schema validation | `pydantic` v2 | Validate API response shapes |

---

## Project Structure

```
playwright_suite/
├── pages/                  # Page Object classes
│   ├── base_page.py        # Shared helpers: navigate, screenshot
│   ├── home_page.py        # Room listing
│   ├── booking_page.py     # Booking form and confirmation
│   ├── admin_page.py       # Admin login and room management
│   └── contact_page.py     # Contact form
├── api/                    # API test helpers
│   ├── client.py           # httpx session wrapper
│   ├── models.py           # Pydantic response models
│   └── endpoints/
│       ├── auth.py
│       ├── booking.py
│       └── room.py
├── tests/
│   ├── ui/
│   │   ├── test_home.py
│   │   ├── test_booking.py
│   │   ├── test_admin.py
│   │   └── test_contact.py
│   └── api/
│       ├── test_auth_api.py
│       ├── test_booking_api.py
│       └── test_room_api.py
├── conftest.py             # All shared fixtures
├── pyproject.toml          # Dependencies + pytest config
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## Target Application

**URL:** https://automationintesting.online
**Admin credentials:** username `admin` / password `password`
**API base:** https://automationintesting.online/api

### UI Surfaces
- **Home page:** Room listing with per-room availability calendar
- **Booking modal:** First name, last name, email, phone, check-in/out date picker
- **Contact form:** Name, email, phone, subject, description
- **Admin panel** (`/admin`): Room CRUD, bookings list, messages inbox, occupancy report

### REST API Endpoints
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/login` | Public | Returns token cookie |
| GET | `/api/booking` | Public | List booking IDs (filterable) |
| POST | `/api/booking` | Public | Create booking |
| GET | `/api/booking/{id}` | Public | Single booking detail |
| PUT | `/api/booking/{id}` | Token | Full update |
| DELETE | `/api/booking/{id}` | Token | Delete → 202 |
| GET | `/api/room` | Public | List all rooms |
| POST | `/api/room` | Token | Create room |
| PUT | `/api/room/{id}` | Token | Update room |
| DELETE | `/api/room/{id}` | Token | Delete room |

---

## Development Phases

### Phase 1 — Foundation (Days 1–3, ~6 hrs)
**Goal:** Prove the environment works before writing real tests.

- **Day 1:** Install dependencies, run `playwright install`, write a single smoke test asserting the page title.
- **Day 2:** Set up folder structure, `conftest.py`, `BasePage`, and `HomePage` POM. Add `base_url` fixture reading from `.env`.
- **Day 3:** Configure `pyproject.toml` with screenshot/tracing options, add `pytest-html`, write the first real test (room cards visible), deliberately break it and inspect the trace.

**Checkpoint:** `pytest -v` runs, one test passes, trace viewer works, HTML report generates.

### Phase 2 — UI Coverage (Days 4–7, ~7 hrs)
**Goal:** All 15 UI test scenarios written and passing.

- **Day 4:** `BookingPage` POM, happy-path booking test with Faker data, date picker via Codegen.
- **Day 5:** Booking negative tests (empty form, invalid dates, past dates). Practice `expect()` auto-retrying assertions.
- **Day 6:** `AdminPage` POM, login tests, room CRUD. Use API for setup state where it speeds things up.
- **Day 7:** `ContactPage` POM, contact form tests, one `page.route()` network interception test. Run full suite three times — fix any flakiness.

**Checkpoint:** All 15 UI scenarios pass consistently. At least one `page.route()` test present.

### Phase 3 — API Coverage (Days 8–12, ~9 hrs)
**Goal:** Full API suite with Pydantic schema validation, edge cases, and remaining UI gaps.

- **Day 8:** `api/client.py` httpx wrapper, session-scoped `auth_token` fixture, `test_auth_api.py`. ✅
- **Day 9:** Pydantic models in `api/models.py`, booking create + read tests with `model_validate()`. ✅
- **Day 10:** DELETE booking; DELETE no-auth → 403; PUT no-auth → 403; GET nonexistent booking → 404; invalid date range → 409/400; overlapping booking → 409. Remove PATCH test (endpoint returns 405 — not implemented on this platform, logged in BUGS.md).
- **Day 11:** Room API tests: list rooms, create room, create room no-auth → 403, PUT room, PUT room no-auth → 403, DELETE room. One cross-layer test: create booking via API → verify in admin UI. Add `parametrize` to at least two tests.
- **Day 12 (UI gaps):** Availability calendar renders; long stay booking (30 nights); admin sees bookings list; contact form submission → verify message appears in admin inbox (cross-layer UI). Optionally: create booking via UI → verify via API.

**Checkpoint:** All API tests pass. Every successful response validated with Pydantic. 403/404/409 edge cases covered. At least two cross-layer tests. All UI gaps closed.

### Phase 4 — CI & Polish (Days 13–15, ~5 hrs)
**Goal:** Production-ready, shareable project.

- **Day 13:** GitHub Actions workflow with matrix strategy (Chromium + Firefox), artifact upload on failure.
- **Day 14:** Dockerfile + `docker-compose.yml`, run full suite in container, add `parametrize` where near-duplicate tests exist.
- **Day 15:** Run `ruff check .` and fix all issues, write README covering all required sections, final full-suite run on both browsers.

**Checkpoint:** GitHub Actions green on both browsers. `docker-compose up` works. `ruff` clean. README complete.

---

## Key Concepts

### Auto-wait (Playwright vs Selenium)
Playwright waits for elements to be actionable before interacting. No `WebDriverWait` or `time.sleep()` needed in most cases.

### Page Object Model
Locators and actions live in a class per page. Tests call methods like `booking_page.submit_form()` instead of raw selectors. A selector change is fixed in one place.

### pytest Fixtures
Shared setup defined in `conftest.py`. Key fixtures and their scopes:
- `browser` — session scope
- `context` — function scope (isolated cookies per test)
- `page` — function scope
- `api_client` — session scope
- `auth_token` — session scope (POST /auth once, reuse token)
- `fake` — function scope (fresh Faker instance per test)

### expect() vs assert
`expect(locator).to_be_visible()` retries automatically until the element appears or timeout is reached. Never use plain `assert` on `.is_visible()` for UI — it fails immediately if the element isn't ready yet.

### API-Assisted Setup
Use the API (fast, direct) to create preconditions for UI tests. Reserve the UI for the assertions. If the setup UI is broken, unrelated tests should not cascade-fail.

### Pydantic for Response Validation
Status codes tell you the request succeeded. `model_validate(response.json())` tells you the response has the right shape. A missing field or wrong type raises `ValidationError` with a precise message.

### Network Interception (page.route)
Playwright can intercept, inspect, and stub network requests at the browser level. Use it to simulate error states (e.g., API returns 500) without needing a real backend failure.

### Session-Scoped Auth
The `auth_token` fixture logs in once per pytest session. All 17 API tests that need authentication share the stored token. Avoids hammering the auth endpoint on every test.

### Cross-Layer Tests
Create data through one channel (API), verify through another (UI). Proves end-to-end consistency. Use sparingly — they're slower — but one or two per project is valuable.

### Test Independence
Every test creates its own data and cleans it up via `yield` fixtures. Tests that share state cascade-fail when one breaks.

### Codegen
`playwright codegen https://automationintesting.online` records interactions and outputs Python. Use it to explore which locator strategy works for tricky elements (like the date picker), then implement it properly inside the Page Object — don't copy the output verbatim.

### Playwright Trace Viewer
On failure with `--tracing=retain-on-failure`, Playwright saves a zip with a full recording of every action, network request, and DOM snapshot. Open with `playwright show-trace trace.zip`. Primary debugging tool.

### Matrix CI Strategy
GitHub Actions matrix runs the same job with different variables in parallel. In this project the variable is the browser name (`chromium`, `firefox`). Ensures tests aren't accidentally browser-specific.

### Docker for Tests
Running in Docker guarantees the same environment everywhere — local, colleague's machine, and CI. Eliminates Python version and system library mismatches.

---

## UI Test Scenarios (18 total)

| File | Scenario | Status |
|---|---|---|
| test_home_ui.py | Room cards visible on load | ✅ |
| test_home_ui.py | Availability calendar renders | Day 12 |
| test_booking_ui.py | Happy path — valid booking | ✅ |
| test_booking_ui.py | Missing required fields | ✅ |
| test_booking_ui.py | Invalid date range | ✅ |
| test_booking_ui.py | Past date rejection | ✅ xfail |
| test_booking_ui.py | Long stay booking (30 nights) | Day 12 |
| test_booking_ui.py | Server error stub (page.route) | ✅ |
| test_admin_ui.py | Admin login — valid credentials | ✅ |
| test_admin_ui.py | Admin login — invalid credentials | ✅ |
| test_admin_ui.py | Create room | ✅ |
| test_admin_ui.py | Edit room price | ✅ |
| test_admin_ui.py | Delete room | ✅ |
| test_admin_ui.py | Admin sees bookings list | Day 12 |
| test_contact_ui.py | Successful contact submission | ✅ |
| test_contact_ui.py | Contact form — missing fields (parametrized) | ✅ |
| test_contact_ui.py | Contact submission → verify in admin inbox | Day 12 |
| test_booking_ui.py | Create booking via UI → verify via API | Day 12 |

---

## API Test Scenarios (19 total)

| File | Scenario | Status |
|---|---|---|
| test_auth_api.py | Valid login returns token cookie | ✅ |
| test_auth_api.py | Invalid password → 401 | ✅ |
| test_auth_api.py | Missing fields → non-200 | ✅ |
| test_booking_api.py | Create booking — happy path | ✅ |
| test_booking_api.py | Get booking by id | ✅ |
| test_booking_api.py | List bookings filtered by roomid | ✅ |
| test_booking_api.py | Full update (PUT) | ✅ |
| test_booking_api.py | PUT without auth → 403 | Day 10 |
| test_booking_api.py | Delete booking | Day 10 |
| test_booking_api.py | Delete without auth → 403 | Day 10 |
| test_booking_api.py | GET nonexistent booking → 404 | Day 10 |
| test_booking_api.py | Invalid date range → 409/400 | Day 10 |
| test_booking_api.py | Overlapping booking conflict → 409 | Day 10 |
| test_room_api.py | List rooms — public | Day 11 |
| test_room_api.py | Create room (admin) | Day 11 |
| test_room_api.py | Create room — no auth → 403 | Day 11 |
| test_room_api.py | Update room (PUT) | Day 11 |
| test_room_api.py | Update room — no auth → 403 | Day 11 |
| test_room_api.py | Delete room | Day 11 |

---

## Documentation Links

| Resource | URL |
|---|---|
| Playwright Python — Full docs | https://playwright.dev/python/docs/intro |
| Playwright — Locators | https://playwright.dev/python/docs/locators |
| Playwright — Assertions (expect) | https://playwright.dev/python/docs/test-assertions |
| Playwright — Network (page.route) | https://playwright.dev/python/docs/network |
| Playwright — Trace Viewer | https://playwright.dev/python/docs/trace-viewer |
| Playwright — Codegen | https://playwright.dev/python/docs/codegen |
| Playwright — Page Object Model | https://playwright.dev/python/docs/pom |
| Playwright — Auth | https://playwright.dev/python/docs/auth |
| Playwright — CI guide | https://playwright.dev/python/docs/ci |
| Playwright — Docker guide | https://playwright.dev/python/docs/docker |
| pytest — Fixtures | https://docs.pytest.org/en/stable/how-to/fixtures.html |
| pytest — parametrize | https://docs.pytest.org/en/stable/how-to/parametrize.html |
| pytest — conftest.py | https://docs.pytest.org/en/stable/reference/fixtures.html |
| httpx — Client | https://www.python-httpx.org/advanced/clients/ |
| Pydantic v2 — Models | https://docs.pydantic.dev/latest/concepts/models/ |
| Faker | https://faker.readthedocs.io/en/master/ |
| ruff | https://docs.astral.sh/ruff/ |
| pytest-html | https://pytest-html.readthedocs.io/en/latest/ |
| Restful Booker Platform — Postman collection (authoritative) | https://www.postman.com/automation-in-testing/restful-booker-collections/collection/ |
| GitHub Actions — Quickstart | https://docs.github.com/en/actions/writing-workflows/quickstart |
| Docker Compose | https://docs.docker.com/compose/gettingstarted/ |

---

## Definition of Done

| Checkpoint | Success Criteria |
|---|---|
| Environment | `playwright install` succeeds; `pytest -v` collects with no import errors |
| UI — Booking | Happy-path test green on Chromium and Firefox |
| UI — Admin | Room CRUD + login tests passing |
| UI — Edge cases | At least 5 negative UI scenarios |
| Network intercept | At least 1 `page.route()` stub test |
| API — Auth | POST /auth tests pass; token fixture reused |
| API — Booking CRUD | All endpoints covered including 409 and 403 guards |
| API — Schemas | Pydantic validates every successful API response |
| CI | GitHub Actions matrix runs Chromium + Firefox; traces upload on failure |
| Reporting | pytest-html generates; screenshots on failed tests |
| README | Setup, .env vars, local run, Docker run, CI badge |
| Code quality | `ruff check .` passes with zero issues |
