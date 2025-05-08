from django.contrib import admin
from .models import AboutRaktaSewa, Notification, FAQ, Gallery, ContactMessage, MobileApp, BloodBankRegistration, Donor, CampSchedule, BloodStock
from django.utils.html import format_html
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect

class RaktaSewaAdminSite(admin.AdminSite):
    site_header = 'RaktaSewa Administration'
    site_title = 'RaktaSewa Admin'
    index_title = 'Welcome to RaktaSewa Administration'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return app_list

    def index(self, request, extra_context=None):
        # If user is authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('admin_dashboard'))
            
        extra_context = extra_context or {}
        extra_context.update({
            'blood_banks_count': BloodBankRegistration.objects.count(),
            'donors_count': Donor.objects.count(),
            'camps_count': CampSchedule.objects.count(),
            'blood_stock_count': BloodStock.objects.count(),
        })
        return super().index(request, extra_context)

admin_site = RaktaSewaAdminSite(name='admin')

# Register your models here
@admin.register(AboutRaktaSewa, site=admin_site)
class AboutRaktaSewaAdmin(admin.ModelAdmin):
    list_display = ("updated_at",)
    fieldsets = (
        (None, {"fields": ("content",)}),
        ("Last Updated", {"fields": ("updated_at",)}),
    )
    readonly_fields = ("updated_at",)

@admin.register(Notification, site=admin_site)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)
    fieldsets = (
        (None, {"fields": ("title", "message")}),
        ("Meta", {"fields": ("created_at",)}),
    )
    readonly_fields = ("created_at",)

@admin.register(FAQ, site=admin_site)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
    search_fields = ("question",)

@admin.register(Gallery, site=admin_site)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("caption", "uploaded_at", "image_tag")
    readonly_fields = ("uploaded_at", "image_tag")
    fieldsets = (
        (None, {"fields": ("image", "caption", "image_tag")}),
        ("Meta", {"fields": ("uploaded_at",)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Preview'

@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "submitted_at")
    search_fields = ("subject", "name", "email")
    readonly_fields = ("submitted_at",)

@admin.register(MobileApp, site=admin_site)
class MobileAppAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short", "download_link")
    search_fields = ("name",)
    
    def description_short(self, obj):
        return obj.description[:50] + ("..." if len(obj.description) > 50 else "")
    description_short.short_description = "Description"

@admin.register(Donor, site=admin_site)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'mobile', 'address', 'bloodbank', 'created_at')
    search_fields = ('name', 'mobile', 'address', 'bloodbank__blood_bank_name')
    list_filter = ('blood_group', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'name', 'profile_picture', 'blood_group', 'address', 'mobile', 'bloodbank', 'created_at'
            )
        }),
    )

@admin.register(CampSchedule, site=admin_site)
class CampScheduleAdmin(admin.ModelAdmin):
    list_display = ('location', 'province', 'district', 'schedule_date', 'start_time', 'end_time', 'bloodbank', 'created_at')
    search_fields = ('location', 'province', 'district', 'bloodbank__blood_bank_name')
    list_filter = ('province', 'district', 'schedule_date', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': (
                'bloodbank', 'province', 'district', 'location', 'schedule_date', 'start_time', 'end_time', 'description', 'created_at'
            )
        }),
    )

@admin.register(BloodBankRegistration, site=admin_site)
class BloodBankRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "blood_bank_name", "city", "district", "province", "contact_person", "email", "submitted_at"
    )
    search_fields = (
        "blood_bank_name", "city", "district", "province", "contact_person", "email"
    )
    list_filter = (
        "province", "district", "category", "submitted_at"
    )
    readonly_fields = (
        "latitude", "longitude", "submitted_at"
    )
    fieldsets = (
        ("Blood Bank Information", {
            "fields": (
                "province", "district", "city", "blood_bank_name", "parent_hospital_name", "short_name", "category",
                "contact_person", "email", "contact_no", "address", "pincode"
            )
        }),
        ("Geographical Location", {
            "fields": ("latitude", "longitude")
        }),
        ("Donation Information", {
            "fields": (
                "donor_voluntary", "donor_replacement", "donor_directed", "donor_autologous", "donor_family", "donor_replacement_external",
                "donation_leucapheresis", "donation_plasmapheresis", "donation_plateletpheresis", "donation_whole_blood", "remark"
            )
        }),
        ("Account", {
            "fields": ("username", "password", "submitted_at")
        }),
    )

@admin.register(BloodStock, site=admin_site)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('bloodbank', 'blood_group', 'units', 'last_updated')
    search_fields = ('bloodbank__blood_bank_name', 'blood_group')
    list_filter = ('blood_group', 'last_updated')
    readonly_fields = ('last_updated',)
    actions = ['delete_selected']
    actions_on_top = True
    actions_on_bottom = False
    fieldsets = (
        (None, {
            'fields': (
                'bloodbank', 'blood_group', 'units', 'last_updated'
            )
        }),
    )
