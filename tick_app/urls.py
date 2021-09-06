from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),

    path('new_ticket/', views.create_new_ticket, name='new_ticket'),
    path('track_my_tickets/', views.customer_ticket_tracking, name='track_my_tickets'),

    path('manage_resources/', views.admin_manage_resources, name='admin_manage_resources'),
    # path('create_category/', views.create_category, name='create_category')

]