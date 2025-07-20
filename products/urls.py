from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products, name='product-list'),  # GET /api/v1/Product
    path('<int:pk>/', views.retrieve_product, name='product-detail'),  # GET /api/v1/Product/:id
    path('create/', views.create_product, name='product-create'),  # POST /api/v1/Product
    path('<int:pk>/update/', views.update_product, name='product-update'),  # PUT /api/v1/Product/:id
    path('<int:pk>/delete/', views.delete_product, name='product-delete'),  # DELETE /api/v1/Product/:id
    path('update-Image-Product/<int:pk>/', views.update_product_image, name='product-update-image'),  # PUT /api/v1/Product/update-Image-Product/:id
    path('my/', views.my_products, name='my-products'),  # GET /api/v1/products/my/
]
