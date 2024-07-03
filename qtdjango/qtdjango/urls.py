"""qtdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .views import load_data
from .views import (
    create_sensor_data,
    read_sensor_data,
    update_sensor_data,
    delete_sensor_data,
    get_all_sensor_data,
    get_sensor_data_paginated,
    get_last_sensor_data,
)

urlpatterns = [
    path("load-data/", load_data, name="load_data"),
    path("sensor-data/", create_sensor_data, name="create_sensor_data"),
    path(
        "sensor-data/<int:sensor_data_id>/", read_sensor_data, name="read_sensor_data"
    ),
    path(
        "sensor-data/<int:sensor_data_id>/",
        update_sensor_data,
        name="update_sensor_data",
    ),
    path(
        "sensor-data/<int:sensor_data_id>/",
        delete_sensor_data,
        name="delete_sensor_data",
    ),
    path("sensor-data-all/", get_all_sensor_data, name="get_all_sensor_data"),
    path(
        "sensor-data-paginated/",
        get_sensor_data_paginated,
        name="get_sensor_data_paginated",
    ),
    path("last-sensor-data/", get_last_sensor_data, name="get_last_sensor_data"),
]
