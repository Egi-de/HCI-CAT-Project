# Edit plan: Convert Flask weather + admin logic to Django

## Information gathered
- `weather/urls.py` expects these endpoints:
  - `''` -> `views.index`
  - `'api/weather-search/'` -> `views.weather_search_api`
  - `'admin/history/'` -> `views.admin_history`
  - `'admin/stats/'` -> `views.admin_stats`
- Current `weather/views.py` contains placeholder implementations for `weather_search_api/admin_history/admin_stats`.
- Current `weather/models.py` is empty.
- `templates/weather/index.html` is now your WeatherSense UI; its JS fetches `/api/weather-search/`.
- `config/settings.py` already has `STATICFILES_DIRS` and `OPENWEATHER_API_KEY`.

## Plan
### Step 1 — Model layer
- Create `SearchHistory` Django model matching Flask fields:
  - `query` (city or "lat,lon")
  - `query_type` ('city'/'coords')
  - `result_city`, `result_country`
  - `temperature`, `condition`
  - `timestamp` (auto_add)
  - `ip_address`
- Add appropriate indexes (optional) for query performance.

### Step 2 — Weather API endpoint
- Replace `weather_search_api` placeholder:
  - Parse request parameters expected by `templates/weather/index.html` JS:
    - if city: `?city=...`
    - if coords: `?lat=...&lon=...`
  - Call OpenWeather via `requests` (same base URL / units metric).
  - Build the JSON response in the structure your UI expects.
    - The current UI JS expects keys like `ok`, and nested `weather` and `location`.
  - Save each successful search to `SearchHistory`.
  - Return meaningful `4xx/5xx` JSON errors.

### Step 3 — Admin endpoints (Django auth)
- Update `admin_history` and `admin_stats`:
  - Restrict to `request.user.is_authenticated and request.user.is_staff`.
  - Implement:
    - `/admin/history/` with pagination (page, per_page=20)
    - `/admin/stats/` computing totals + top cities + today count
  - Create templates:
    - `templates/weather/admin_login.html` OR use Django’s built-in admin auth pages.
    - `templates/weather/admin_dashboard.html`
    - `templates/weather/admin_history.html`
  - If you keep custom `/admin/login`, implement it with username/password and `User`.
  - Implement delete endpoint (note: current `weather/urls.py` does not include delete URL; we may add it).

### Step 4 — URL wiring / templates
- If needed, extend `weather/urls.py` to include missing routes from the UI:
  - delete: `/admin/delete/<int:id>/`.
  - dashboard: `/admin/dashboard/` (currently UI links to `/admin/dashboard`).
- Ensure templates render and variables match.

### Step 5 — Migrations + verification
- Run `python manage.py makemigrations weather && python manage.py migrate`.
- Smoke test:
  - GET `/` renders UI.
  - Call `/api/weather-search/?city=London` returns expected JSON.
  - Search writes to DB.
  - Admin stats/history pages show correct counts.

## Dependent files to edit
- `weather/models.py`
- `weather/views.py`
- `weather/urls.py`
- Add templates under `templates/weather/` for admin pages.

## Followup steps
- Run migrations.
- Start dev server and verify the end-to-end flow.

