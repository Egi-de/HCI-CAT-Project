# TODO

## Fix Django startup error (missing view functions)
- [x] Implement missing Django views referenced by `weather/urls.py`.
- [x] `python manage.py check` passes.

## UI wiring
- [x] Update `templates/weather/index.html` to your WeatherSense “index” HTML.
- [ ] Ensure the index page works end-to-end with the weather API endpoint and admin pages.

## Convert Flask to Django (core app logic)
- [ ] Create Django model(s) equivalent to Flask:
  - [ ] SearchHistory model
  - [ ] Admin auth (use Django User or custom model)
- [ ] Implement `/api/weather-search/` to call OpenWeather and return the JSON format the index JS expects.
- [ ] Save each successful search into SearchHistory (include query, type, result fields, timestamp, ip).
- [ ] Implement admin pages:
  - [ ] `/admin/login` (if custom) OR use Django auth views + custom templates
  - [ ] `/admin/dashboard`
  - [ ] `/admin/history`
  - [ ] `/admin/delete/<id>`
- [ ] Lock admin pages with `is_staff`/permissions.

## Testing
- [ ] Run `python manage.py runserver` and verify:
  - [ ] GET `/` renders the UI
  - [ ] POST `/api/weather-search/` returns correct JSON
  - [ ] History records appear in `/admin/history`
  - [ ] Stats counters update in `/admin/dashboard`

