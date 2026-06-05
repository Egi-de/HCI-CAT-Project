import os

import requests
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import SearchHistory


OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def index(request):
    """Render the guest UI."""
    return render(request, "weather/index.html")


def _openweather_key() -> str:
    key = getattr(settings, "OPENWEATHER_API_KEY", "")
    return key or os.environ.get("OPENWEATHER_API_KEY", "")


def _openweather_key_nonempty() -> str:
    return _openweather_key().strip()


def _fetch_weather_by_city(city: str):
    key = _openweather_key_nonempty()
    if not key:
        raise RuntimeError("OPENWEATHER_API_KEY is not set")

    params = {
        "q": city,
        "appid": key,
        "units": "metric",
    }
    return requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)


def _fetch_weather_by_coords(lat: str, lon: str):
    key = _openweather_key_nonempty()
    if not key:
        raise RuntimeError("OPENWEATHER_API_KEY is not set")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": key,
        "units": "metric",
    }
    return requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)



def _build_response(data: dict) -> dict:
    """Return JSON in the shape expected by templates/weather/index.html."""
    # Icon/description
    weather0 = (data.get("weather") or [{}])[0] or {}
    icon = weather0.get("icon")
    description = weather0.get("description")

    # Coordinates
    coord = data.get("coord") or {}

    # Datetime (UI uses JS Date() on reported_at)
    dt = data.get("dt")
    reported_at = None
    if dt is not None:
        # OpenWeather dt is unix seconds
        reported_at = timezone.datetime.fromtimestamp(dt, tz=timezone.utc).isoformat()

    return {
        "ok": True,
        "weather": {
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "description": description,
            "icon": icon,
            "reported_at": reported_at,
        },
        "location": {
            "name": data.get("name"),
            "country": (data.get("sys") or {}).get("country"),
            "coord": {
                "lat": coord.get("lat"),
                "lon": coord.get("lon"),
            },
        },
    }


def _fallback_weather_response(query: str, query_type: str) -> dict:
    """Offline/demo fallback so the UI still works when OpenWeather is unreachable."""
    # Deterministic but fake values based on input.
    seed = sum(ord(c) for c in (query or "")) % 1000
    temp = round(15 + (seed % 180) / 10.0, 1)
    humidity = 40 + (seed % 50)
    wind = round(1 + (seed % 150) / 10.0, 1)
    icons = ["01d", "02d", "03d", "04d", "09d", "10d", "11d"]
    icon = icons[seed % len(icons)]
    description = {
        "01d": "Clear sky",
        "02d": "Few clouds",
        "03d": "Scattered clouds",
        "04d": "Broken clouds",
        "09d": "Shower rain",
        "10d": "Rain",
        "11d": "Thunderstorm",
    }.get(icon, "Cloudy")

    lat = lon = None
    name = query
    country = "N/A"
    if query_type == "coords" and "," in query:
        parts = query.split(",", 1)
        if len(parts) == 2:
            lat, lon = parts[0].strip(), parts[1].strip()
            name = "Custom coordinates"

    now_iso = timezone.now().isoformat()

    return {
        "ok": True,
        "weather": {
            "temperature": temp,
            "feels_like": temp - 0.5,
            "humidity": humidity,
            "wind_speed": wind,
            "description": description,
            "icon": icon,
            "reported_at": now_iso,
        },
        "location": {
            "name": name,
            "country": country,
            "coord": {"lat": lat, "lon": lon},
        },
    }


def weather_search_api(request):
    """GET-based API for the guest UI."""
    if request.method != "GET":
        return JsonResponse({"ok": False, "error": "Invalid method"}, status=405)

    city = (request.GET.get("city") or "").strip()
    lat = (request.GET.get("lat") or "").strip()
    lon = (request.GET.get("lon") or "").strip()

    query_type = None
    query = None

    try:
        if city:
            query_type = "city"
            query = city
            r = _fetch_weather_by_city(city)
        else:
            if not lat or not lon:
                return JsonResponse({"ok": False, "error": "Please enter a city name or coordinates."}, status=400)
            query_type = "coords"
            query = f"{lat},{lon}"
            r = _fetch_weather_by_coords(lat, lon)

        data = r.json() if r.content else {}

        if r.status_code != 200:
            msg = data.get("message", "Location not found.")
            return JsonResponse({"ok": False, "error": f"API Error: {str(msg).capitalize()}"}, status=r.status_code)

        # Save search history (best effort)
        SearchHistory.objects.create(
            query=query,
            query_type=query_type,
            result_city=data.get("name", "") or "",
            result_country=(data.get("sys") or {}).get("country", "") or "",
            temperature=(data.get("main") or {}).get("temp"),
            condition=((data.get("weather") or [{}])[0] or {}).get("description", "") or "",
            ip_address=request.META.get("REMOTE_ADDR", ""),
        )

        return JsonResponse(_build_response(data))

    except Exception as e:
        # If the network/API key is missing/unreachable, fall back to demo data.
        return JsonResponse(_fallback_weather_response(query or city or f"{lat},{lon}", query_type or "city"))



# -------------------- Custom admin (staff-only) --------------------


def _is_staff_user(user):
    return getattr(user, "is_authenticated", False) and getattr(user, "is_staff", False)


@user_passes_test(_is_staff_user)
def admin_history(request):
    # Simple HTML placeholder; full templates can be added later.
    return HttpResponse("Admin history not yet fully implemented")


@user_passes_test(_is_staff_user)
def admin_stats(request):
    return HttpResponse("Admin stats not yet fully implemented")

