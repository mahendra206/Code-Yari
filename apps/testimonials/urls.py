from django.urls import path
from . import views
app_name = 'testimonials'
urlpatterns = [
    path('', views.testimonials_list, name='list'),
]
