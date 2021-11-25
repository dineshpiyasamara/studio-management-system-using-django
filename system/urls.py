from django.contrib import admin
from django.urls import path
from system import views
from .views import MpPasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),

    path('purchase/', views.purchase, name='purchase'),

    path('sell/', views.sell, name='sell'),


    path('inventory/', views.items, name='inventory'),
    path('inventory/<str:product>/', views.item_selling_price, name='sellingprice'),

    path('employees/', views.employee, name='employees'),
    path('employees/add/', views.registerUser, name='register'),
    path('employees/<str:name>/', views.editUser, name='edit'),
    path('employees/<str:name>/change-password/',
         MpPasswordChangeView.as_view(), name='password'),
    path('employees/remove/<str:name>/', views.delete_user, name='delete_user'),

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('item-json/', views.json_item_data, name='item-json'),
    path('other-item-json/<str:product>/',
         views.json_item_data_others, name='other-item-json'),
]
