from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.add_to_cart, name='cart-add'),  # POST /api/v1/Cart/:ProductId
    path('', views.list_cart, name='cart-list'),  # GET /api/v1/Cart/
    path('clear/', views.clear_cart, name='cart-clear'),  # PUT /api/v1/Cart/clear
    path('<int:product_id>/delete/', views.remove_from_cart, name='cart-remove'),  # DELETE /api/v1/Cart/:ProductId
] 