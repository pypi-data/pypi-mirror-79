from django.urls import path
from . import views

urlpatterns = [
    path('adoptions/', views.home, name='home'),

    path('adoptions/<int:pet_id>/', views.pet_detail , name = 'pet_detail')


]