from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_categories, name='category-list'),  # GET /api/v1/Category
    path('create/', views.create_category, name='category-create'),  # POST /api/v1/Category
    path('<int:pk>/', views.retrieve_category, name='category-detail'),  # GET /api/v1/Category/:id
    path('<int:pk>/update/', views.update_category, name='category-update'),  # PUT /api/v1/Category/:id
    path('update-Image-Category/<int:pk>/', views.update_category_image, name='category-update-image'),  # PUT /api/v1/Category/update-Image-Category/:id
    path('<int:pk>/delete/', views.delete_category, name='category-delete'),  # DELETE /api/v1/Category/:id
    path('<int:pk>/Products/', views.list_category_products, name='category-products'),  # GET /api/v1/Category/:id/Products
] 