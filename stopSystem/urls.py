from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('dash/', views.streamilit_view, name='streamilit_view'),
]


