from .views import *
from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name = 'category'),
    path('product-detail/<slug>',ProductDetailView.as_view(), name="product-detail"),
    path('product_review', product_review, name='product_review'),
    path('search_product',SearchProduct.as_view(), name='search_product'),
    path('cart', CartView.as_view(), name='cart'),
    path('signup', signup, name='signup'),
    path('add_cart/<slug>',cart, name='add_cart'),
    path('delete_cart/<slug>', delete_cart, name='delete_cart'),
    path('reduce_quantity/<slug>', reduce_quantity, name='reduce_quantity'),


]
