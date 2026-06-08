# TODO — WeatherSense HCI Admin Dashboard Upgrade

## Step 1 — Fix guest UI
- [x] Remove duplicated/invalid second UI in `templates/weather/index.html` (everything after the first closing `</html>`).
- [x] Ensure the remaining HTML/JS only references existing element IDs.

## Step 2 — Upgrade admin UI styling
- [x] Add missing dashboard-focused CSS classes in `static/weather/app.css` (kpi cards, table styling, badges, responsive grids).
- [x] Refactor `templates/weather/admin_dashboard.html`, `admin_history.html`, `admin_stats.html` to use those classes (minimal inline styles).

## Step 3 — Validate
- [x] Run migrations (only if needed) and start server.
- [x] Manually verify: guest search works + history pages populate + admin dashboard loads without layout glitches.

