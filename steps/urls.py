from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboardAPI, name="dashboard"),
    path("user/", views.userAPI, name="user"),
    path("selfdash/", views.selfDashboardAPI, name="selfdash"),
    path('delete/<int:pk>/', views.deleteStepAPI, name='delete'),
    path('create/', views.createStepAPI, name='create')
]