from django.urls import path
from . import views
app_name = 'leads'
urlpatterns = [
    path('get-a-quote/', views.get_quote, name='get_quote'),
]
