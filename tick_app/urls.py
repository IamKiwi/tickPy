from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('new_ticket/', views.create_new_ticket, name='new_ticket'),
    path('track_my_tickets/', views.customer_ticket_tracking, name='track_my_tickets'),
    path('show_ticket/<str:pk>', views.show_ticket, name='show_ticket'),
    path('abandon_ticket/<str:pk>', views.abandon_ticket, name='abandon_ticket'),
    path('resolve_ticket/<str:pk>', views.resolve_ticket, name='resolve_ticket'),
    path('assign_ticket/<str:pk>', views.assign_ticket, name='assign_ticket'),
    path('engineer_queue_tracking/', views.engineer_queue_tracking, name='engineer_queue_tracking'),
    path('add_comment/<str:pk>', views.add_comment_to_ticket, name='add_comment'),

    path('manage_resources/', views.admin_manage_resources, name='admin_manage_resources'),
    path('decom_resource/<str:pk>', views.admin_decom_resource, name='admin_decom_resource'),
    path('manage_queues/', views.admin_manage_queues, name='admin_manage_queues'),
    path('manage_users/', views.admin_manage_users, name='admin_manage_users'),
    # path('create_category/', views.create_category, name='create_category')

]
