# TODO — WeatherSense Admin Dashboard Upgrade

## Next steps (planned)
1. Update `admin_history` backend to support filters: date range, condition substring, location
2. Update `weather_search_api` to anonymize IP before saving
3. Update `admin_history.html` UI to support collapsible per-group view + improved per-group aggregates
4. Add real-time dashboard charts:
   - new staff-only JSON endpoint for chart aggregates/time-bucketed counts
   - update `admin_dashboard.html` to render charts (Chart.js) with polling
5. Run the app and verify guest search, admin history grouping/filtering, and real-time chart updates

