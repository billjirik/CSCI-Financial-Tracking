from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]
urlpatterns += [
    path('register/', views.register, name='register'),
    
]


