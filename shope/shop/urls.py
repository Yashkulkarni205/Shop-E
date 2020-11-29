from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/detail', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update', views.product_update, name='product-update'),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    path('products/<str:category>/', views.ProductByCategory.as_view(), name='product-category'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('check-out/', views.checkout, name='check-out'),
    path('orders/', views.orders, name='orders'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)