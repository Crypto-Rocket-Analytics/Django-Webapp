"""rocket-webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('data_fresh/', views.data_fresh, name="data_fresh"),
    path('full_data_fresh/', views.full_data_fresh, name="full_data_fresh"),
    path('api/tracker/data/', views.tracker, name="tracker"),
    path('click/add/', views.add_button_click, name="add_button_click"),
    path('click/calculate/', views.calculate_button_click, name="calculate_button_click"),
    path('add/data/fleet/', views.getTrackerData, name="getTrackerData"),
]
