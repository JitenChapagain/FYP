from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from core.models import BloodBankRegistration, Donor, BloodStock, CampSchedule, PROVINCE_CHOICES, DISTRICT_CHOICES, AboutRaktaSewa, Notification, FAQ, Gallery, ContactMessage, MobileApp
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from core.forms import BloodBankRegistrationForm, DonorForm, CampScheduleForm, BloodStockForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage

# Create your views here.

@staff_member_required
def admin_dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    total_blood_banks = BloodBankRegistration.objects.count()
    total_donors = Donor.objects.count()
    total_camps = CampSchedule.objects.count()
    
    # Get total blood units across all blood banks
    total_blood_units = sum(stock.units for stock in BloodStock.objects.all())
    
    # Get recent activities
    recent_activities = []
    
    # Add recent blood bank registrations
    recent_blood_banks = BloodBankRegistration.objects.order_by('-submitted_at')[:3]
    for bank in recent_blood_banks:
        recent_activities.append({
            'description': f'New blood bank registered: {bank.blood_bank_name}',
            'timestamp': bank.submitted_at
        })
    
    # Add recent donors
    recent_donors = Donor.objects.order_by('-created_at')[:3]
    for donor in recent_donors:
        recent_activities.append({
            'description': f'New donor registered: {donor.name} ({donor.blood_group})',
            'timestamp': donor.created_at
        })
    
    # Add upcoming camps
    upcoming_camps = CampSchedule.objects.filter(schedule_date__gte=timezone.now().date()).order_by('schedule_date')[:3]
    for camp in upcoming_camps:
        # Convert date to datetime for consistent comparison
        camp_datetime = timezone.make_aware(timezone.datetime.combine(camp.schedule_date, timezone.datetime.min.time()))
        recent_activities.append({
            'description': f'Upcoming blood donation camp at {camp.location}',
            'timestamp': camp_datetime
        })
    
    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    context = {
        'total_users': total_users,
        'total_blood_banks': total_blood_banks,
        'total_donors': total_donors,
        'total_camps': total_camps,
        'total_blood_units': total_blood_units,
        'recent_activities': recent_activities[:5],  # Show only 5 most recent activities
    }
    
    return render(request, 'dashboard/admindashboard.html', context)

@staff_member_required
def admin_blood_banks(request):
    # Get all blood banks
    blood_banks = BloodBankRegistration.objects.all().order_by('-submitted_at')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        blood_banks = blood_banks.filter(
            Q(blood_bank_name__icontains=search_query) |
            Q(province__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(contact_no__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Get entries per page from request, default to 10
    entries_per_page = request.GET.get('entries', '10')
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(blood_banks, int(entries_per_page))
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blood_banks': page_obj,
        'search_query': search_query,
        'total_blood_banks': blood_banks.count(),
        'entries': entries_per_page,
        'filtered_count': blood_banks.count(),
        'is_filtered': bool(search_query),
    }
    return render(request, 'blood_banks/adminBloodBanks.html', context)

@staff_member_required
def blood_bank_delete(request, pk):
    blood_bank = get_object_or_404(BloodBankRegistration, pk=pk)
    if request.method == 'POST':
        blood_bank.delete()
        messages.success(request, 'Blood bank deleted successfully.')
    return redirect('admin_blood_banks')

@staff_member_required
def blood_bank_view(request, pk):
    blood_bank = get_object_or_404(BloodBankRegistration, pk=pk)
    context = {
        'blood_bank': blood_bank
    }
    return render(request, 'blood_banks/adminBloodBankDetail.html', context)

@staff_member_required
def blood_bank_edit(request, pk):
    blood_bank = get_object_or_404(BloodBankRegistration, pk=pk)
    
    if request.method == 'POST':
        # Update basic information
        blood_bank.blood_bank_name = request.POST.get('blood_bank_name')
        blood_bank.parent_hospital_name = request.POST.get('parent_hospital_name')
        blood_bank.short_name = request.POST.get('short_name')
        blood_bank.category = request.POST.get('category')
        
        # Update contact information
        blood_bank.contact_person = request.POST.get('contact_person')
        blood_bank.email = request.POST.get('email')
        blood_bank.contact_no = request.POST.get('contact_no')
        
        # Update location information
        blood_bank.province = request.POST.get('province')
        blood_bank.district = request.POST.get('district')
        blood_bank.city = request.POST.get('city')
        blood_bank.address = request.POST.get('address')
        blood_bank.pincode = request.POST.get('pincode')
        blood_bank.latitude = float(request.POST.get('latitude'))
        blood_bank.longitude = float(request.POST.get('longitude'))
        
        # Update donor types
        blood_bank.donor_voluntary = 'donor_voluntary' in request.POST
        blood_bank.donor_replacement = 'donor_replacement' in request.POST
        blood_bank.donor_directed = 'donor_directed' in request.POST
        blood_bank.donor_autologous = 'donor_autologous' in request.POST
        blood_bank.donor_family = 'donor_family' in request.POST
        blood_bank.donor_replacement_external = 'donor_replacement_external' in request.POST
        
        # Update donation methods
        blood_bank.donation_leucapheresis = 'donation_leucapheresis' in request.POST
        blood_bank.donation_plasmapheresis = 'donation_plasmapheresis' in request.POST
        blood_bank.donation_plateletpheresis = 'donation_plateletpheresis' in request.POST
        blood_bank.donation_whole_blood = 'donation_whole_blood' in request.POST
        
        # Update account information
        blood_bank.username = request.POST.get('username')
        new_password = request.POST.get('password')
        if new_password:  # Only update password if a new one is provided
            blood_bank.password = new_password
        
        # Update remarks
        blood_bank.remark = request.POST.get('remark', '')
        
        try:
            blood_bank.save()
            messages.success(request, 'Blood bank updated successfully.')
            return redirect('admin_blood_banks')
        except Exception as e:
            messages.error(request, f'Error updating blood bank: {str(e)}')
    
    # Get province and district choices from the model
    
    context = {
        'blood_bank': blood_bank,
        'PROVINCE_CHOICES': PROVINCE_CHOICES,
        'DISTRICT_CHOICES': DISTRICT_CHOICES
    }
    return render(request, 'blood_banks/adminBloodBankEdit.html', context)

@staff_member_required
def blood_bank_add(request):
    if request.method == 'POST':
        form = BloodBankRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Blood bank added successfully.')
                return redirect('admin_blood_banks')
            except Exception as e:
                messages.error(request, f'Error adding blood bank: {str(e)}')
        else:
            # Log form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BloodBankRegistrationForm()
    
    context = {
        'form': form,
        'PROVINCE_CHOICES': PROVINCE_CHOICES,
        'DISTRICT_CHOICES': DISTRICT_CHOICES
    }
    return render(request, 'blood_banks/adminBloodBankAdd.html', context)

def admin_logout(request):
    logout(request)
    return redirect('/admin/login/?next=/admin/')

@staff_member_required
def admin_donors(request):
    # Get all donors
    donors = Donor.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        donors = donors.filter(
            Q(name__icontains=search_query) |
            Q(blood_group__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(bloodbank__blood_bank_name__icontains=search_query)
        )
    
    # Get entries per page from request, default to 10
    entries_per_page = request.GET.get('entries', '10')
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(donors, int(entries_per_page))
    page_obj = paginator.get_page(page_number)
    
    context = {
        'donors': page_obj,
        'search_query': search_query,
        'total_donors': donors.count(),
        'entries': entries_per_page,
        'filtered_count': donors.count(),
        'is_filtered': bool(search_query),
    }
    return render(request, 'donors/adminDonors.html', context)

@staff_member_required
def donor_view(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    context = {
        'donor': donor
    }
    return render(request, 'donors/adminDonorDetail.html', context)

@staff_member_required
def donor_edit(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor updated successfully.')
            return redirect('admin_donors')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DonorForm(instance=donor)
    
    context = {
        'form': form,
        'donor': donor
    }
    return render(request, 'donors/adminDonorEdit.html', context)

@staff_member_required
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Donor deleted successfully.')
    return redirect('admin_donors')

@staff_member_required
def donor_add(request):
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Donor added successfully.')
                return redirect('admin_donors')
            except Exception as e:
                messages.error(request, f'Error adding donor: {str(e)}')
        else:
            # Log form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DonorForm()
    
    context = {
        'form': form
    }
    return render(request, 'donors/adminDonorAdd.html', context)

@staff_member_required
def admin_camps(request):
    # Get all camps
    camps = CampSchedule.objects.all().order_by('-schedule_date')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        camps = camps.filter(
            Q(location__icontains=search_query) |
            Q(province__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(bloodbank__blood_bank_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get entries per page from request, default to 10
    entries_per_page = request.GET.get('entries', '10')
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(camps, int(entries_per_page))
    page_obj = paginator.get_page(page_number)
    
    context = {
        'camps': page_obj,
        'search_query': search_query,
        'total_camps': camps.count(),
        'entries': entries_per_page,
        'filtered_count': camps.count(),
        'is_filtered': bool(search_query),
        'now': timezone.now(),  # Add current time to context
    }
    return render(request, 'camps/adminCamps.html', context)

@staff_member_required
def camp_view(request, pk):
    camp = get_object_or_404(CampSchedule, pk=pk)
    context = {
        'camp': camp
    }
    return render(request, 'camps/adminCampDetail.html', context)

@staff_member_required
def camp_edit(request, pk):
    camp = get_object_or_404(CampSchedule, pk=pk)
    
    if request.method == 'POST':
        form = CampScheduleForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Camp schedule updated successfully.')
            return redirect('admin_camps')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CampScheduleForm(instance=camp)
    
    context = {
        'form': form,
        'camp': camp
    }
    return render(request, 'camps/adminCampEdit.html', context)

@staff_member_required
def camp_add(request):
    if request.method == 'POST':
        form = CampScheduleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Camp schedule added successfully.')
                return redirect('admin_camps')
            except Exception as e:
                messages.error(request, f'Error adding camp schedule: {str(e)}')
        else:
            # Log form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CampScheduleForm()
    
    context = {
        'form': form
    }
    return render(request, 'camps/adminCampAdd.html', context)

@staff_member_required
def camp_delete(request, pk):
    camp = get_object_or_404(CampSchedule, pk=pk)
    if request.method == 'POST':
        camp.delete()
        messages.success(request, 'Camp schedule deleted successfully.')
    return redirect('admin_camps')

@staff_member_required
def admin_blood_stocks(request):
    # Get all blood stocks with their blood banks
    blood_stocks = BloodStock.objects.select_related('bloodbank').all().order_by('-last_updated')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        blood_stocks = blood_stocks.filter(
            Q(bloodbank__blood_bank_name__icontains=search_query) |
            Q(blood_group__icontains=search_query) |
            Q(bloodbank__province__icontains=search_query) |
            Q(bloodbank__district__icontains=search_query)
        )
    
    # Get entries per page from request, default to 10
    entries_per_page = request.GET.get('entries', '10')
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(blood_stocks, int(entries_per_page))
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blood_stocks': page_obj,
        'search_query': search_query,
        'total_stocks': blood_stocks.count(),
        'entries': entries_per_page,
        'filtered_count': blood_stocks.count(),
        'is_filtered': bool(search_query),
    }
    return render(request, 'blood_stocks/adminBloodStocks.html', context)

@staff_member_required
def blood_stock_view(request, pk):
    blood_stock = get_object_or_404(BloodStock, pk=pk)
    context = {
        'blood_stock': blood_stock
    }
    return render(request, 'blood_stocks/adminBloodStockDetail.html', context)

@staff_member_required
def blood_stock_edit(request, pk):
    blood_stock = get_object_or_404(BloodStock, pk=pk)
    
    if request.method == 'POST':
        form = BloodStockForm(request.POST, instance=blood_stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood stock updated successfully.')
            return redirect('admin_blood_stocks')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BloodStockForm(instance=blood_stock)
    
    context = {
        'form': form,
        'blood_stock': blood_stock
    }
    return render(request, 'blood_stocks/adminBloodStockEdit.html', context)

@staff_member_required
def blood_stock_add(request):
    if request.method == 'POST':
        form = BloodStockForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Blood stock added successfully.')
                return redirect('admin_blood_stocks')
            except Exception as e:
                messages.error(request, f'Error adding blood stock: {str(e)}')
        else:
            # Log form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BloodStockForm()
    
    context = {
        'form': form
    }
    return render(request, 'blood_stocks/adminBloodStockAdd.html', context)

@staff_member_required
def blood_stock_delete(request, pk):
    blood_stock = get_object_or_404(BloodStock, pk=pk)
    if request.method == 'POST':
        blood_stock.delete()
        messages.success(request, 'Blood stock deleted successfully.')
    return redirect('admin_blood_stocks')

# About Rakta Sewa Views
@login_required(login_url='admin_login')
def admin_about_raktasewa(request):
    about_contents = AboutRaktaSewa.objects.all().order_by('-updated_at')
    context = {
        'about_contents': about_contents
    }
    return render(request, 'about_raktasewa/adminAboutRaktaSewa.html', context)

@login_required(login_url='admin_login')
def admin_about_raktasewa_add(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        
        about = AboutRaktaSewa.objects.create(
            content=content
        )
        messages.success(request, 'About content added successfully!')
        return redirect('admin_about_raktasewa')
    
    return render(request, 'about_raktasewa/adminAboutRaktaSewaAdd.html')

@login_required(login_url='admin_login')
def admin_about_raktasewa_detail(request, about_id):
    about = get_object_or_404(AboutRaktaSewa, id=about_id)
    context = {
        'about': about
    }
    return render(request, 'about_raktasewa/adminAboutRaktaSewaDetail.html', context)

@login_required(login_url='admin_login')
def admin_about_raktasewa_edit(request, about_id):
    about = get_object_or_404(AboutRaktaSewa, id=about_id)
    
    if request.method == 'POST':
        about.title = request.POST.get('title')
        about.description = request.POST.get('description')
        about.save()
        
        messages.success(request, 'About content updated successfully!')
        return redirect('admin_about_raktasewa_detail', about_id=about.id)
    
    context = {
        'about': about
    }
    return render(request, 'about_raktasewa/adminAboutRaktaSewaEdit.html', context)

@login_required(login_url='admin_login')
def admin_about_raktasewa_delete(request, about_id):
    about = get_object_or_404(AboutRaktaSewa, id=about_id)
    about.delete()
    messages.success(request, 'About content deleted successfully!')
    return redirect('admin_about_raktasewa')

# Notification Views
@login_required(login_url='admin_login')
def admin_notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/adminNotifications.html', context)

@login_required(login_url='admin_login')
def admin_notification_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        
        notification = Notification.objects.create(
            title=title,
            message=message
        )
        messages.success(request, 'Notification added successfully!')
        return redirect('admin_notifications')
    
    return render(request, 'notifications/adminNotificationAdd.html')

@login_required(login_url='admin_login')
def admin_notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    context = {
        'notification': notification
    }
    return render(request, 'notifications/adminNotificationDetail.html', context)

@login_required(login_url='admin_login')
def admin_notification_edit(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    
    if request.method == 'POST':
        notification.title = request.POST.get('title')
        notification.message = request.POST.get('message')
        notification.save()
        
        messages.success(request, 'Notification updated successfully!')
        return redirect('admin_notification_detail', notification_id=notification.id)
    
    context = {
        'notification': notification
    }
    return render(request, 'notifications/adminNotificationEdit.html', context)

@login_required(login_url='admin_login')
def admin_notification_delete(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    messages.success(request, 'Notification deleted successfully!')
    return redirect('admin_notifications')

@login_required
def admin_faqs(request):
    faqs = FAQ.objects.all().order_by('-id')
    return render(request, 'faqs/adminFaqs.html', {'faqs': faqs})

@login_required
def admin_faq_add(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        
        if not question or not answer:
            messages.error(request, 'Please fill in all fields')
            return redirect('admin_faq_add')
            
        FAQ.objects.create(question=question, answer=answer)
        messages.success(request, 'FAQ added successfully')
        return redirect('admin_faqs')
        
    return render(request, 'faqs/adminFaqAdd.html')

@login_required
def admin_faq_detail(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    return render(request, 'faqs/adminFaqDetail.html', {'faq': faq})

@login_required
def admin_faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        
        if not question or not answer:
            messages.error(request, 'Please fill in all fields')
            return redirect('admin_faq_edit', faq_id=faq_id)
            
        faq.question = question
        faq.answer = answer
        faq.save()
        
        messages.success(request, 'FAQ updated successfully')
        return redirect('admin_faq_detail', faq_id=faq_id)
        
    return render(request, 'faqs/adminFaqEdit.html', {'faq': faq})

@login_required
def admin_faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    messages.success(request, 'FAQ deleted successfully')
    return redirect('admin_faqs')

@login_required
def admin_gallery(request):
    # Get the number of entries per page from request, default to 5
    entries_per_page = int(request.GET.get('entries', 5))
    
    # Get all gallery items ordered by upload date
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')
    
    # Get search query if any
    search_query = request.GET.get('search', '')
    if search_query:
        gallery_items = gallery_items.filter(caption__icontains=search_query)
    
    # Get total count before pagination
    total_gallery_items = gallery_items.count()
    
    # Paginate the queryset
    paginator = Paginator(gallery_items, entries_per_page)
    page = request.GET.get('page', 1)
    
    try:
        gallery_items = paginator.page(page)
    except PageNotAnInteger:
        gallery_items = paginator.page(1)
    except EmptyPage:
        gallery_items = paginator.page(paginator.num_pages)
    
    context = {
        'gallery_items': gallery_items,
        'total_gallery_items': total_gallery_items,
        'is_filtered': bool(search_query),
        'search_query': search_query,
        'filtered_count': gallery_items.paginator.count if search_query else total_gallery_items,
        'entries_per_page': entries_per_page,
    }
    
    return render(request, 'gallery/adminGallery.html', context)

@login_required
def admin_gallery_add(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            caption = request.POST.get('caption')

            if not image:
                messages.error(request, 'Please select an image')
                return redirect('admin_gallery_add')

            gallery_item = Gallery.objects.create(
                image=image,
                caption=caption
            )
            messages.success(request, 'Gallery item added successfully')
            return redirect('admin_gallery')
        except Exception as e:
            messages.error(request, f'Error adding gallery item: {str(e)}')
            return redirect('admin_gallery_add')

    return render(request, 'gallery/adminGalleryAdd.html')

@login_required
def admin_gallery_detail(request, pk):
    gallery_item = get_object_or_404(Gallery, pk=pk)
    return render(request, 'gallery/adminGalleryDetail.html', {'gallery_item': gallery_item})

@login_required
def admin_gallery_edit(request, pk):
    gallery_item = get_object_or_404(Gallery, pk=pk)
    
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            caption = request.POST.get('caption')

            if image:
                gallery_item.image = image
            gallery_item.caption = caption
            gallery_item.save()
            
            messages.success(request, 'Gallery item updated successfully')
            return redirect('admin_gallery')
        except Exception as e:
            messages.error(request, f'Error updating gallery item: {str(e)}')
            return redirect('admin_gallery_edit', pk=pk)

    return render(request, 'gallery/adminGalleryEdit.html', {'gallery_item': gallery_item})

@login_required
def admin_gallery_delete(request, pk):
    gallery_item = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        try:
            gallery_item.delete()
            messages.success(request, 'Gallery item deleted successfully')
        except Exception as e:
            messages.error(request, f'Error deleting gallery item: {str(e)}')
    return redirect('admin_gallery')

@login_required(login_url='admin_login')
def admin_contact_messages(request):
    contact_messages = ContactMessage.objects.all().order_by('-submitted_at')
    context = {
        'contact_messages': contact_messages
    }
    return render(request, 'contact_messages/adminContactMessages.html', context)

@login_required(login_url='admin_login')
def admin_contact_message_detail(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    context = {
        'contact_message': contact_message
    }
    return render(request, 'contact_messages/adminContactMessageDetail.html', context)

@login_required(login_url='admin_login')
def admin_contact_message_delete(request, pk):
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    contact_message.delete()
    messages.success(request, 'Contact message deleted successfully!')
    return redirect('admin_contact_messages')

# Mobile App Views
@login_required(login_url='admin_login')
def admin_mobile_apps(request):
    mobile_apps = MobileApp.objects.all().order_by('-id')
    context = {
        'mobile_apps': mobile_apps
    }
    return render(request, 'mobile_apps/adminMobileApps.html', context)

@login_required(login_url='admin_login')
def admin_mobile_app_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        download_link = request.POST.get('download_link')
        
        if not name or not description or not download_link:
            messages.error(request, 'Please fill in all required fields')
            return redirect('admin_mobile_app_add')
            
        mobile_app = MobileApp.objects.create(
            name=name,
            description=description,
            download_link=download_link
        )
        messages.success(request, 'Mobile app added successfully!')
        return redirect('admin_mobile_app_detail', pk=mobile_app.id)
    
    return render(request, 'mobile_apps/adminMobileAppAdd.html')

@login_required(login_url='admin_login')
def admin_mobile_app_detail(request, pk):
    mobile_app = get_object_or_404(MobileApp, pk=pk)
    context = {
        'mobile_app': mobile_app
    }
    return render(request, 'mobile_apps/adminMobileAppDetail.html', context)

@login_required(login_url='admin_login')
def admin_mobile_app_edit(request, pk):
    mobile_app = get_object_or_404(MobileApp, pk=pk)
    
    if request.method == 'POST':
        mobile_app.name = request.POST.get('name')
        mobile_app.description = request.POST.get('description')
        mobile_app.download_link = request.POST.get('download_link')
        mobile_app.save()
        
        messages.success(request, 'Mobile app updated successfully!')
        return redirect('admin_mobile_app_detail', pk=mobile_app.id)
    
    context = {
        'mobile_app': mobile_app
    }
    return render(request, 'mobile_apps/adminMobileAppEdit.html', context)

@login_required(login_url='admin_login')
def admin_mobile_app_delete(request, pk):
    mobile_app = get_object_or_404(MobileApp, pk=pk)
    mobile_app.delete()
    messages.success(request, 'Mobile app deleted successfully!')
    return redirect('admin_mobile_apps')
