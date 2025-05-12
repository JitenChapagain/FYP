from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bloodbank/home/', views.bloodbank_home, name='bloodbank_home'),
    path('about/', views.about, name='about'),
    path('notification/', views.notification, name='notification'),
    path('faq/', views.faq, name='faq'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('apps/', views.apps, name='apps'),
    # Placeholder URLs for dropdowns (implement as needed)
    path('directory/', views.bloodbank_directory, name='bloodbank_directory'),
    path('camp/', views.home, name='camp'),
    path('donor-login/', views.home, name='donor_login'),
    path('about-donation/', views.home, name='about_donation'),
    path('raktasewa-login/', views.raktasewa_login, name='raktasewa_login'),
    path('bloodbank/', views.bloodbank_dashboard, name='bloodbank_dashboard'),
    path('bloodbank/profile/', views.bloodbank_profile, name='bloodbank_profile'),
    path('bloodbank-logout/', views.bloodbank_logout, name='bloodbank_logout'),
    path('add-donor/', views.add_donor, name='add_donor'),
    path('donor-list/', views.donor_list, name='donor_list'),
    path('camp-schedules/', views.camp_schedules, name='camp_schedules'),
    path('update-blood/', views.update_blood, name='update_blood'),
    path('update-blood-group/<str:blood_group>/', views.update_blood_group, name='update_blood_group'),
    path('blood-stock-list/', views.blood_stock_list, name='blood_stock_list'),
    path('add-camp/', views.add_camp, name='add_camp'),
    path('edit-camp/<int:camp_id>/', views.edit_camp, name='edit_camp'),
    path('delete-camp/<int:camp_id>/', views.delete_camp, name='delete_camp'),
    path('add-bank/', views.add_bank, name='add_bank'),
    path('availability/', views.bloodavailability, name='bloodavailability'),
    path('bloodbank/<int:bloodbank_id>/', views.bloodbank_detail, name='bloodbank_detail'),
]
