from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_orders, name='order-list'),  # GET /api/v1/Order
    path('create/', views.create_order, name='order-create'),  # POST /api/v1/Order
    path('<int:pk>/', views.retrieve_order, name='order-detail'),  # GET /api/v1/Order/:orderId
    path('<int:pk>/delete/', views.delete_order, name='order-delete'),  # DELETE /api/v1/Order/:orderId
    path('<int:pk>/<str:status_str>/', views.update_order_status, name='order-update-status'),  # PUT /api/v1/Order/:orderId/:status
    path('total/', views.get_order_total, name='order-total'),  # GET /api/v1/Order/total
    path('user/<int:user_id>/', views.list_orders_by_user, name='order-list-by-user'),  # GET /api/v1/Order/:userId
    path('Product/<int:product_id>/count/', views.list_orders_by_product, name='order-list-by-product'),  # GET /api/v1/Order/Product/:productId/count
    path('status/<str:status_str>/', views.list_orders_by_status, name='order-list-by-status'),  # GET /api/v1/Order/status/:status
    path('user/<int:user_id>/status/<str:status_str>/', views.list_user_orders_by_status, name='order-list-user-status'),  # GET /api/v1/user/:userId/status/:status
] 