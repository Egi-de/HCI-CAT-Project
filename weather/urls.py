from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='weather-home'),
    path('api/weather-search/', views.weather_search_api, name='weather-search-api'),

    # Custom administrator auth & pages (NOT Django admin)
    path('admin/login/', views.admin_login, name='admin-login'),
    path('admin/signup/', views.admin_signup, name='admin-signup'),
    path('admin/logout/', views.admin_logout_view, name='admin-logout'),

    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/history/', views.admin_history, name='admin-history'),
    path('admin/stats/', views.admin_stats, name='admin-stats'),
]



