from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('blood-banks/', views.admin_blood_banks, name='admin_blood_banks'),
    path('blood-banks/view/<int:pk>/', views.blood_bank_view, name='blood_bank_view'),
    path('blood-banks/edit/<int:pk>/', views.blood_bank_edit, name='blood_bank_edit'),
    path('blood-banks/add/', views.blood_bank_add, name='blood_bank_add'),
    path('blood-banks/delete/<int:pk>/', views.blood_bank_delete, name='blood_bank_delete'),
    
    path('donors/', views.admin_donors, name='admin_donors'),
    path('donors/view/<int:pk>/', views.donor_view, name='donor_view'),
    path('donors/edit/<int:pk>/', views.donor_edit, name='donor_edit'),
    path('donors/add/', views.donor_add, name='donor_add'),
    path('donors/delete/<int:pk>/', views.donor_delete, name='donor_delete'),
    
    path('camps/', views.admin_camps, name='admin_camps'),
    path('camps/view/<int:pk>/', views.camp_view, name='camp_view'),
    path('camps/edit/<int:pk>/', views.camp_edit, name='camp_edit'),
    path('camps/add/', views.camp_add, name='camp_add'),
    path('camps/delete/<int:pk>/', views.camp_delete, name='camp_delete'),
    
    path('blood-stocks/', views.admin_blood_stocks, name='admin_blood_stocks'),
    path('blood-stocks/view/<int:pk>/', views.blood_stock_view, name='blood_stock_view'),
    path('blood-stocks/edit/<int:pk>/', views.blood_stock_edit, name='blood_stock_edit'),
    path('blood-stocks/add/', views.blood_stock_add, name='blood_stock_add'),
    path('blood-stocks/delete/<int:pk>/', views.blood_stock_delete, name='blood_stock_delete'),
    
    path('about-raktasewa/', views.admin_about_raktasewa, name='admin_about_raktasewa'),
    path('about-raktasewa/add/', views.admin_about_raktasewa_add, name='admin_about_raktasewa_add'),
    path('about-raktasewa/<int:about_id>/', views.admin_about_raktasewa_detail, name='admin_about_raktasewa_detail'),
    path('about-raktasewa/<int:about_id>/edit/', views.admin_about_raktasewa_edit, name='admin_about_raktasewa_edit'),
    path('about-raktasewa/<int:about_id>/delete/', views.admin_about_raktasewa_delete, name='admin_about_raktasewa_delete'),
    
    path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('notifications/add/', views.admin_notification_add, name='admin_notification_add'),
    path('notifications/<int:notification_id>/', views.admin_notification_detail, name='admin_notification_detail'),
    path('notifications/<int:notification_id>/edit/', views.admin_notification_edit, name='admin_notification_edit'),
    path('notifications/<int:notification_id>/delete/', views.admin_notification_delete, name='admin_notification_delete'),
    
    path('logout/', views.admin_logout, name='admin_logout'),
    path('faqs/', views.admin_faqs, name='admin_faqs'),
    path('faqs/add/', views.admin_faq_add, name='admin_faq_add'),
    path('faqs/<int:faq_id>/', views.admin_faq_detail, name='admin_faq_detail'),
    path('faqs/<int:faq_id>/edit/', views.admin_faq_edit, name='admin_faq_edit'),
    path('faqs/<int:faq_id>/delete/', views.admin_faq_delete, name='admin_faq_delete'),
    
    # Gallery URLs
    path('gallery/', views.admin_gallery, name='admin_gallery'),
    path('gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('gallery/<int:pk>/', views.admin_gallery_detail, name='admin_gallery_detail'),
    path('gallery/<int:pk>/edit/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('gallery/<int:pk>/delete/', views.admin_gallery_delete, name='admin_gallery_delete'),

    # Contact Messages URLs
    path('contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('contact-messages/<int:pk>/', views.admin_contact_message_detail, name='admin_contact_message_detail'),
    path('contact-messages/<int:pk>/delete/', views.admin_contact_message_delete, name='admin_contact_message_delete'),

    # Mobile App URLs
    path('mobile-apps/', views.admin_mobile_apps, name='admin_mobile_apps'),
    path('mobile-apps/add/', views.admin_mobile_app_add, name='admin_mobile_app_add'),
    path('mobile-apps/<int:pk>/', views.admin_mobile_app_detail, name='admin_mobile_app_detail'),
    path('mobile-apps/<int:pk>/edit/', views.admin_mobile_app_edit, name='admin_mobile_app_edit'),
    path('mobile-apps/<int:pk>/delete/', views.admin_mobile_app_delete, name='admin_mobile_app_delete'),
] 