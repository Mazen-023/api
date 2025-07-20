from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('me/profile/', views.user_profile, name='user-profile'),
    path('me/profile/update/', views.update_profile, name='user-profile-update'),  # PUT /api/v1/User/me/profile/update/
    path('me/activate/', views.activate_account, name='user-activate'),  # POST /api/v1/User/me/activate
    path('me/profile/update-image/', views.update_profile_image, name='user-update-image'),  # POST /api/v1/User/me/profile/update-image
    path('me/deactivate/', views.deactivate_account, name='user-deactivate'),  # DELETE /api/v1/User/me/deactivate
    path('admin/changePassword/<int:user_id>/', views.admin_change_password, name='admin-change-password'),  # POST /api/v1/User/admin/changePassword/:id
    path('admin/', views.admin_create_user, name='admin-create'),  # POST /api/v1/User/admin
    path('admin/<int:user_id>/', views.admin_get_user, name='admin-get'),  # GET /api/v1/User/admin/:id
    path('admin/<int:user_id>/delete/', views.admin_delete_user, name='admin-delete'),  # DELETE /api/v1/User/admin/:id
    path('admin/<int:user_id>/update/', views.admin_update_user, name='admin-update'),  # PUT /api/v1/User/admin/:id
]
