from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('income_expenses/', views.income_expense_list, name='income_expense_list'),
]
urlpatterns += [
    path('register/', views.register, name='register'),
    
]



