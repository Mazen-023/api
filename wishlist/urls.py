from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.add_to_wishlist, name='wishlist-add'),  # POST /api/v1/Wishlist/:ProductId
    path('<int:product_id>/delete/', views.remove_from_wishlist, name='wishlist-remove'),  # DELETE /api/v1/Wishlist/:ProductId
    path('', views.list_wishlist, name='wishlist-list'),  # GET /api/v1/Wishlist/
] 