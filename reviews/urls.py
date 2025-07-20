from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_all_reviews, name='review-list-all'),  # GET /api/v1/Review/
    path('<int:product_id>/', views.add_review, name='review-add'),  # POST /api/v1/Review/:productId
    path('<int:product_id>/list/', views.list_reviews, name='review-list'),  # GET /api/v1/Review/:productId
    path('<int:review_id>/update/', views.update_review, name='review-update'),  # PUT /api/v1/Review/:reviewId
    path('<int:review_id>/delete/', views.delete_review, name='review-delete'),  # DELETE /api/v1/Review/:reviewId
    path('my/list/', views.my_reviews, name='my-reviews-list'),  # GET /api/v1/Review/my/list/
    path('<int:product_id>/my/', views.my_review_for_product, name='my-review-for-product'),  # GET /api/v1/Review/<product_id>/my/
] 