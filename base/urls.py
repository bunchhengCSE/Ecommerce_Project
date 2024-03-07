from django.urls import path
from . import views
app_name = 'base'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('shop/', views.shop_page, name='shop_page'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),


    path('shop/<int:pk>/', views.detail_product, name='detail_product_page'),
    path('cart/', views.cart_page, name='cart_page'),
    path('shop/update_product/',views.update_product,name='update_product'),
]