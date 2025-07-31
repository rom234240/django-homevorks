from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.SensorListCreateView.as_view()),
    path('sensors/<int:pk>/', views.SensorRetrieveUpdateView.as_view()),
    path('measurements/', views.MeasurementCreateView.as_view()),
]