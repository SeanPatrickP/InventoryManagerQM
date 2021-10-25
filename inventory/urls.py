from django.urls import path

from . import views

urlpatterns = [
    path('items/', views.getItems, name='getItems'),
    path('getItemsCount/', views.getItemsCount, name='getItemsCount'),
    path('addItem/', views.addItem, name='addItem'),
    path('insertItem/', views.insertItem, name='insertItem'),
    path('deleteItem/', views.deleteItem, name='deleteItem'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('sellItems/', views.sellItems, name='sellItems'),
    path('addItemToSell/', views.addItemToSell, name='addItemToSell'),
    path('sellSelected/', views.sellSelected, name='sellSelected'),
    path('', views.index, name='index'),
]