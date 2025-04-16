from django.urls import path
from . import views
from .views import index

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
]
