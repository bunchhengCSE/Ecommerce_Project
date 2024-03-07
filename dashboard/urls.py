from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('insert-product/',views.insert_product,name='insert-product'),
    path('update_product/<int:pk>/',views.update_product,name='update_product'),
    path('remove_product/<int:pk>/',views.remove_product,name='remove_product'),
]