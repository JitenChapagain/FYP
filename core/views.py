from django.shortcuts import render, redirect
from .models import AboutRaktaSewa, Notification, FAQ, Gallery, MobileApp, Donor, BloodBankRegistration, CampSchedule, BloodStock
from .forms import ContactForm, BloodBankRegistrationForm, DonorForm, CampScheduleForm, BloodStockForm
from .bloodbank_forms import BloodBankLoginForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.db.models import Q
import django.db.models as models

# Province and District choices
PROVINCE_CHOICES = [
    ('1', 'Province No. 1 — Koshi Province'),
    ('2', 'Province No. 2 — Madhesh Province'),
    ('3', 'Province No. 3 — Bagmati Province'),
    ('4', 'Province No. 4 — Gandaki Province'),
    ('5', 'Province No. 5 — Lumbini Province'),
    ('6', 'Province No. 6 — Karnali Province'),
    ('7', 'Province No. 7 — Sudurpashchim Province'),
]

DISTRICT_CHOICES = {
    '1': [
        ('bhojpur', 'Bhojpur'),
        ('dhankuta', 'Dhankuta'),
        ('ilam', 'Ilam'),
        ('jhapa', 'Jhapa'),
        ('khotang', 'Khotang'),
        ('morang', 'Morang'),
        ('okhaldhunga', 'Okhaldhunga'),
        ('panchthar', 'Panchthar'),
        ('sankhuwasabha', 'Sankhuwasabha'),
        ('solukhumbu', 'Solukhumbu'),
        ('sunsari', 'Sunsari'),
        ('taplejung', 'Taplejung'),
        ('terhathum', 'Terhathum'),
        ('udayapur', 'Udayapur')
    ],
    '2': [
        ('bara', 'Bara'),
        ('dhanusha', 'Dhanusha'),
        ('mahottari', 'Mahottari'),
        ('parsa', 'Parsa'),
        ('rautahat', 'Rautahat'),
        ('saptari', 'Saptari'),
        ('sarlahi', 'Sarlahi'),
        ('siraha', 'Siraha')
    ],
    '3': [
        ('bhaktapur', 'Bhaktapur'),
        ('chitwan', 'Chitwan'),
        ('dhading', 'Dhading'),
        ('dolakha', 'Dolakha'),
        ('kathmandu', 'Kathmandu'),
        ('kavrepalanchok', 'Kavrepalanchok'),
        ('lalitpur', 'Lalitpur'),
        ('makwanpur', 'Makwanpur'),
        ('nuwakot', 'Nuwakot'),
        ('ramechhap', 'Ramechhap'),
        ('rasuwa', 'Rasuwa'),
        ('sindhuli', 'Sindhuli'),
        ('sindhupalchok', 'Sindhupalchok')
    ],
    '4': [
        ('baglung', 'Baglung'),
        ('gorkha', 'Gorkha'),
        ('kaski', 'Kaski'),
        ('lamjung', 'Lamjung'),
        ('manang', 'Manang'),
        ('mustang', 'Mustang'),
        ('myagdi', 'Myagdi'),
        ('nawalparasi_east', 'Nawalpur (Nawalparasi East)'),
        ('parbat', 'Parbat'),
        ('syangja', 'Syangja'),
        ('tanahun', 'Tanahun')
    ],
    '5': [
        ('arghakhanchi', 'Arghakhanchi'),
        ('banke', 'Banke'),
        ('bardiya', 'Bardiya'),
        ('dang', 'Dang'),
        ('eastern_rukum', 'Eastern Rukum'),
        ('gulmi', 'Gulmi'),
        ('kapilvastu', 'Kapilvastu'),
        ('palpa', 'Palpa'),
        ('parasi', 'Parasi (Nawalparasi West)'),
        ('pyuthan', 'Pyuthan'),
        ('rolpa', 'Rolpa'),
        ('rupandehi', 'Rupandehi')
    ],
    '6': [
        ('dailekh', 'Dailekh'),
        ('dolpa', 'Dolpa'),
        ('humla', 'Humla'),
        ('jajarkot', 'Jajarkot'),
        ('jumla', 'Jumla'),
        ('kalikot', 'Kalikot'),
        ('mugu', 'Mugu'),
        ('salyan', 'Salyan'),
        ('surkhet', 'Surkhet'),
        ('western_rukum', 'Western Rukum')
    ],
    '7': [
        ('achham', 'Achham'),
        ('baitadi', 'Baitadi'),
        ('bajhang', 'Bajhang'),
        ('bajura', 'Bajura'),
        ('dadeldhura', 'Dadeldhura'),
        ('darchula', 'Darchula'),
        ('doti', 'Doti'),
        ('kailali', 'Kailali'),
        ('kanchanpur', 'Kanchanpur')
    ]
}

def home(request):
    return render(request, 'home.html')

def bloodavailability(request):
    # Get search parameters
    province = request.GET.get('province')
    district = request.GET.get('district')
    blood_group = request.GET.get('blood_group')
    
    # Get unique provinces from the database
    provinces = BloodBankRegistration.objects.values('province').distinct()
    available_provinces = []
    
    # Create a mapping of province names to codes
    province_name_to_code = {name: code for code, name in PROVINCE_CHOICES}
    
    for p in provinces:
        province_value = p['province']
        # Get the display name from PROVINCE_CHOICES
        province_display_name = next((name for code, name in PROVINCE_CHOICES if code == province_value), province_value)
        available_provinces.append((province_value, province_display_name))
    
    # Get unique districts for the selected province (or all if no province selected)
    available_districts = []
    district_queryset = BloodBankRegistration.objects.all()

    if province:
        # Filter by the selected province code
        district_queryset = district_queryset.filter(province=province)
        
        # Get the list of districts specific to the selected province from the static choices
        province_specific_district_choices = dict(DISTRICT_CHOICES.get(province, []))
        
        # Fetch distinct district codes present in the DB for this province
        districts_in_db = district_queryset.values_list('district', flat=True).distinct()
        
        # Create the choices list using names from the static choices for districts found in DB
        for district_code in districts_in_db:
            district_name = province_specific_district_choices.get(district_code, district_code) # Fallback to code if name not found
            available_districts.append((district_code, district_name))
            
    else:
        # If no province is selected, get all distinct district codes from DB
        all_districts_in_db = district_queryset.values_list('district', flat=True).distinct()
        
        # Create a flat map of all district codes to names for easier lookup
        all_district_choices_map = {}
        for p_code, d_list in DISTRICT_CHOICES.items():
            all_district_choices_map.update(dict(d_list))
            
        # Create the choices list using names from the static map
        for district_code in all_districts_in_db:
            district_name = all_district_choices_map.get(district_code, district_code) # Fallback to code
            available_districts.append((district_code, district_name))

    # Sort districts alphabetically by name
    available_districts.sort(key=lambda x: x[1])
    
    # Handle province and district filtering for the main blood bank query
    # Initialize with all bloodbanks
    bloodbanks_query = BloodBankRegistration.objects.all()

    # Apply province filter if a specific province is selected
    if province:
        bloodbanks_query = bloodbanks_query.filter(province=province)
        
    # Apply district filter if a specific district is selected (independent of province)
    if district:
        bloodbanks_query = bloodbanks_query.filter(district=district)
    
    # Handle blood group filtering (if needed, apply to the already filtered query)
    if blood_group:
        bloodbanks_query = bloodbanks_query.filter(
            blood_stock__blood_group=blood_group
        ).distinct()
    
    # Get unique blood groups for the search results
    blood_groups = set()
    # Iterate over the final queryset result
    for bloodbank in bloodbanks_query:
        if hasattr(bloodbank, 'blood_stock'):
            for stock in bloodbank.blood_stock.all():
                blood_groups.add(stock.blood_group)
    
    context = {
        'bloodbanks': bloodbanks_query, # Pass the final filtered queryset
        'blood_groups': blood_groups,
        'province': province,
        'district': district,
        'blood_group': blood_group,
        'PROVINCE_CHOICES': available_provinces,
        'DISTRICT_CHOICES': available_districts,
        'BLOOD_GROUP_CHOICES': BloodStock.BLOOD_GROUP_CHOICES
    }
    return render(request, 'bloodavailability.html', context)

def bloodbank_directory(request):
    # Get search parameters
    province = request.GET.get('province')
    district = request.GET.get('district')
    
    # Get unique provinces from the database
    provinces = BloodBankRegistration.objects.values('province').distinct()
    available_provinces = []
    
    # Create a mapping of province names to codes
    province_name_to_code = {name: code for code, name in PROVINCE_CHOICES}
    
    for p in provinces:
        province_value = p['province']
        # Get the display name from PROVINCE_CHOICES
        province_display_name = next((name for code, name in PROVINCE_CHOICES if code == province_value), province_value)
        available_provinces.append((province_value, province_display_name))
    
    # Get unique districts for the selected province (or all if no province selected)
    available_districts = []
    district_queryset = BloodBankRegistration.objects.all()

    if province:
        # Filter by the selected province code
        district_queryset = district_queryset.filter(province=province)
        
        # Get the list of districts specific to the selected province from the static choices
        province_specific_district_choices = dict(DISTRICT_CHOICES.get(province, []))
        
        # Fetch distinct district codes present in the DB for this province
        districts_in_db = district_queryset.values_list('district', flat=True).distinct()
        
        # Create the choices list using names from the static choices for districts found in DB
        for district_code in districts_in_db:
            district_name = province_specific_district_choices.get(district_code, district_code) # Fallback to code if name not found
            available_districts.append((district_code, district_name))
            
    else:
        # If no province is selected, get all distinct district codes from DB
        all_districts_in_db = district_queryset.values_list('district', flat=True).distinct()
        
        # Create a flat map of all district codes to names for easier lookup
        all_district_choices_map = {}
        for p_code, d_list in DISTRICT_CHOICES.items():
            all_district_choices_map.update(dict(d_list))
            
        # Create the choices list using names from the static map
        for district_code in all_districts_in_db:
            district_name = all_district_choices_map.get(district_code, district_code) # Fallback to code
            available_districts.append((district_code, district_name))

    # Sort districts alphabetically by name
    available_districts.sort(key=lambda x: x[1])
    
    # Handle province and district filtering for the main blood bank query
    # Initialize with all bloodbanks
    bloodbanks_query = BloodBankRegistration.objects.all()

    # Apply province filter if a specific province is selected
    if province:
        bloodbanks_query = bloodbanks_query.filter(province=province)
        
    # Apply district filter if a specific district is selected (independent of province)
    if district:
        bloodbanks_query = bloodbanks_query.filter(district=district)
    
    context = {
        'bloodbanks': bloodbanks_query,
        'province': province,
        'district': district,
        'PROVINCE_CHOICES': available_provinces,
        'DISTRICT_CHOICES': available_districts,
    }
    return render(request, 'bloodbankdirectory.html', context)

def bloodbank_detail(request, bloodbank_id):
    bloodbank = get_object_or_404(BloodBankRegistration, id=bloodbank_id)
    return render(request, 'bloodbank_detail.html', {
        'bloodbank': bloodbank
    })

def about(request):
    about = AboutRaktaSewa.objects.last()
    return render(request, 'about.html', {'about': about})

def notification(request):
    notifications = Notification.objects.order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def gallery(request):
    images = Gallery.objects.order_by('-uploaded_at')
    return render(request, 'gallery.html', {'images': images})

def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()  # reset form
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'success': success})

def apps(request):
    apps = MobileApp.objects.all()
    return render(request, 'apps.html', {'apps': apps})


def add_bank(request):
    success = False
    if request.method == 'POST':
        form = BloodBankRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = BloodBankRegistrationForm()  # reset form after successful submission
    else:
        form = BloodBankRegistrationForm()
    return render(request, 'add_bank.html', {'form': form, 'success': success})


def raktasewa_login(request):
    error = None
    if request.method == 'POST':
        form = BloodBankLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = BloodBankRegistration.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['bloodbank_user_id'] = user.id
                    return redirect('bloodbank_home')
                else:
                    error = "Invalid credentials."
            except BloodBankRegistration.DoesNotExist:
                error = "Invalid credentials."

def update_blood(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    
    # Get blood group choices and their stock
    blood_groups = []
    for blood_group in BloodStock.BLOOD_GROUP_CHOICES:
        try:
            stock = BloodStock.objects.get(
                bloodbank=bloodbank,
                blood_group=blood_group[0]
            )
            units = stock.units
        except BloodStock.DoesNotExist:
            units = 0
        
        blood_groups.append({
            'group': blood_group[1],
            'code': blood_group[0],
            'units': units
        })
    
    return render(request, 'update_blood.html', {
        'blood_groups': blood_groups
    })

def update_blood_group(request, blood_group):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    
    try:
        blood_stock = BloodStock.objects.get(
            bloodbank=bloodbank,
            blood_group=blood_group
        )
    except BloodStock.DoesNotExist:
        blood_stock = BloodStock(
            bloodbank=bloodbank,
            blood_group=blood_group,
            units=0
        )
    
    if request.method == 'POST':
        form = BloodStockForm(request.POST, instance=blood_stock)
        if form.is_valid():
            form.save()
            return redirect('update_blood')
    else:
        form = BloodStockForm(instance=blood_stock)
    
    return render(request, 'update_blood_group.html', {
        'form': form,
        'blood_group': blood_group
    })

def blood_stock_list(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    blood_stock = BloodStock.objects.filter(bloodbank=bloodbank)
    
    return render(request, 'blood_stock_list.html', {
        'blood_stock': blood_stock
    })

def add_donor(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    success = None
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.bloodbank = bloodbank  # assign logged-in blood bank
            donor.save()
            success = True
            form = DonorForm()  # reset form
        else:
            success = False
    else:
        form = DonorForm()
    return render(request, 'add_donor.html', {'form': form, 'success': success})

def bloodbank_home(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)

    # Total units
    total_units = BloodStock.objects.filter(bloodbank=bloodbank).aggregate(total=models.Sum('units'))['total'] or 0
    # Notifications for this blood bank (customize as needed)
    notifications = Notification.objects.filter(bloodbank=bloodbank).order_by('-created_at') if hasattr(Notification, 'bloodbank') else Notification.objects.all().order_by('-created_at')
    # Donor count for this blood bank (customize as needed)
    donor_count = Donor.objects.filter(bloodbank=bloodbank).count() if hasattr(Donor, 'bloodbank') else Donor.objects.count()

    context = {
        'user': bloodbank,
        'total_units': total_units,
        'notifications': notifications,
        'donor_count': donor_count,
    }
    return render(request, 'bloodbank_home.html', context)

def bloodbank_dashboard(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    
    # Get blood stock data
    blood_stock = BloodStock.objects.filter(bloodbank=bloodbank)
    
    return render(request, 'bloodbank.html', {
        'bloodbank_name': bloodbank.blood_bank_name,
        'blood_stock': blood_stock
    })


def bloodbank_profile(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    user = BloodBankRegistration.objects.get(id=user_id)

    if request.method == 'POST':
        # Use the registration form for editing, but exclude password field
        from .forms import BloodBankRegistrationForm
        form = BloodBankRegistrationForm(request.POST, instance=user)
        form.fields['password'].required = False
        if form.is_valid():
            # Only update password if provided
            if form.cleaned_data['password']:
                user.password = form.cleaned_data['password']
            form.save()
            success = True
        else:
            success = False
    else:
        from .forms import BloodBankRegistrationForm
        form = BloodBankRegistrationForm(instance=user)
        form.fields['password'].required = False
        form.fields['password'].widget.attrs['placeholder'] = 'Leave blank to keep current password'
        success = None
    return render(request, 'bloodbank_profile.html', {'form': form, 'user': user, 'success': success})

def bloodbank_logout(request):
    request.session.flush()
    return redirect('raktasewa_login')

def donor_list(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    donors = Donor.objects.filter(bloodbank=bloodbank).order_by('-created_at')
    return render(request, 'donor_list.html', {'donors': donors})

def camp_schedules(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    camps = CampSchedule.objects.filter(bloodbank=bloodbank).order_by('-schedule_date')
    return render(request, 'camp_schedules.html', {
        'camps': camps,
        'form': CampScheduleForm()
    })

def add_camp(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    if request.method == 'POST':
        form = CampScheduleForm(request.POST)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.bloodbank = bloodbank
            camp.save()
            return redirect('camp_schedules')
    return redirect('camp_schedules')

def edit_camp(request, camp_id):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    camp = get_object_or_404(CampSchedule, id=camp_id, bloodbank=bloodbank)
    
    if request.method == 'POST':
        form = CampScheduleForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('camp_schedules')
    else:
        form = CampScheduleForm(instance=camp)
    
    return render(request, 'edit_camp.html', {
        'form': form,
        'camp': camp
    })

def delete_camp(request, camp_id):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    camp = get_object_or_404(CampSchedule, id=camp_id, bloodbank=bloodbank)
    if request.method == 'POST':
        camp.delete()
    return redirect('camp_schedules')

def update_blood(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    
    # Get blood group choices and their stock
    blood_groups = []
    for blood_group in BloodStock.BLOOD_GROUP_CHOICES:
        try:
            stock = BloodStock.objects.get(
                bloodbank=bloodbank,
                blood_group=blood_group[0]
            )
            units = stock.units
        except BloodStock.DoesNotExist:
            units = 0
        
        blood_groups.append({
            'group': blood_group[1],
            'code': blood_group[0],
            'units': units
        })
    
    return render(request, 'update_blood.html', {
        'blood_groups': blood_groups
    })

def update_blood_group(request, blood_group):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    
    try:
        blood_stock = BloodStock.objects.get(
            bloodbank=bloodbank,
            blood_group=blood_group
        )
    except BloodStock.DoesNotExist:
        blood_stock = BloodStock(
            bloodbank=bloodbank,
            blood_group=blood_group,
            units=0
        )
    
    if request.method == 'POST':
        form = BloodStockForm(request.POST, instance=blood_stock)
        if form.is_valid():
            form.save()
            return redirect('update_blood')
    else:
        form = BloodStockForm(instance=blood_stock)
    
    return render(request, 'update_blood_group.html', {
        'form': form,
        'blood_group': blood_group
    })

def blood_stock_list(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    blood_stock = BloodStock.objects.filter(bloodbank=bloodbank)
    
    return render(request, 'blood_stock_list.html', {
        'blood_stock': blood_stock
    })

def add_donor(request):
    user_id = request.session.get('bloodbank_user_id')
    if not user_id:
        return redirect('raktasewa_login')
    bloodbank = BloodBankRegistration.objects.get(id=user_id)
    success = None
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.bloodbank = bloodbank  # assign logged-in blood bank
            donor.save()
            success = True
            form = DonorForm()  # reset form
        else:
            success = False
    else:
        form = DonorForm()
    return render(request, 'add_donor.html', {'form': form, 'success': success})
