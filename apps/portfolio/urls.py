from django.urls import path
from . import views
app_name = 'portfolio'
urlpatterns = [
    path('', views.portfolio_list, name='list'),
    path('case-studies/', views.case_studies_view, name='case_studies'),
    path('<slug:slug>/', views.portfolio_detail, name='detail'),
]

