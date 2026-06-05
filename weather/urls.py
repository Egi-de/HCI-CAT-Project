from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='weather-home'),
    path('api/weather-search/', views.weather_search_api, name='weather-search-api'),
    path('admin/history/', views.admin_history, name='admin-history'),
    path('admin/stats/', views.admin_stats, name='admin-stats'),
]


