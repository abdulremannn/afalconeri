from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('systems/', views.systems, name='systems'),
    path('capabilities/', views.capabilities, name='capabilities'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('command/login/', views.admin_login, name='admin_login'),
    path('command/logout/', views.admin_logout, name='admin_logout'),
    path('command/', views.admin_dashboard, name='admin_dashboard'),
    path('command/systems/', views.admin_systems, name='admin_systems'),
    path('command/systems/<str:system_id>/', views.admin_system_edit, name='admin_system_edit'),
    path('command/capabilities/', views.admin_capabilities, name='admin_capabilities'),
    path('command/capabilities/<int:cap_id>/', views.admin_capability_edit, name='admin_capability_edit'),
    path('command/contact/', views.admin_contact, name='admin_contact'),
]
