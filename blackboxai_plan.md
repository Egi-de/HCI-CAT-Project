# Admin guest history: multi-city view

## Information gathered
- Guest searches are persisted in `weather.models.SearchHistory`.
- `weather.views.admin_dashboard` currently shows only aggregates (total count, query types, top conditions).
- `weather.views.admin_history` currently shows the last 200 rows with no way to group by city/search.

## Goal
On the admin UI:
1. Show total search count.
2. On the History page, show *multiple cities* the guest users searched for, with their associated records.

## Edit plan (files)
### 1) `weather/views.py`
- Update `admin_history` to:
  - group rows by `query` + `query_type`
  - include count per group
  - show latest timestamp per group
  - still provide the underlying rows for each group so the admin can see “records for those cities”.

### 2) `templates/weather/admin_history.html`
- Replace the flat table with a grouped table:
  - City/Query (display `query`)
  - Type
  - Count
  - Latest time
  - Expandable section (or second table per group) listing each record’s result + condition + ip.

### 3) `templates/weather/admin_dashboard.html` (optional, minimal)
- Ensure it keeps showing total search count.
- (No major changes required for this task since “total search” is already present.)

## Followup steps
- Run `python manage.py makemigrations` / `migrate` only if models changed (not expected).
- Run server and test by performing 4 city searches as guest.
- Verify admin History shows those 4 city groups with their rows.
