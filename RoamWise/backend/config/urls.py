from django.urls import path
from tourism import views
urlpatterns = [
 path('api/health/', views.health), path('api/bootstrap/', views.bootstrap),
 path('api/trips/', views.trips), path('api/trips/<int:trip_id>/', views.trip_detail),
 path('api/trips/<int:trip_id>/recover/', views.recover), path('api/trips/<int:trip_id>/expenses/', views.expenses),
 path('api/trips/<int:trip_id>/votes/', views.votes), path('api/business-submissions/', views.business_submissions),
 path('api/reports/', views.reports), path('api/assistant/', views.assistant),
 path('api/auth/register/', views.auth_register), path('api/auth/login/', views.auth_login),
 path('api/auth/logout/', views.auth_logout), path('api/auth/me/', views.auth_me),
]
