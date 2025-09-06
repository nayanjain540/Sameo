from django.urls import path
from .views import category_selection_view, form_view
from .admin_views import admin_login, admin_logout, admin_dashboard, admin_form_detail

urlpatterns = [
    path('', category_selection_view, name='category_selection'),
    path('form/', form_view, name='form_page'),    
    # Admin URLs
    path('sameo_admin/', admin_login, name='admin_login'),
    path('sameo_admin/logout/', admin_logout, name='admin_logout'),
    path('sameo_admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('sameo_admin/form/<str:form_id>/', admin_form_detail, name='admin_form_detail'),
]
