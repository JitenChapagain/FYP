from django import forms
from .models import ContactMessage, BloodBankRegistration, PROVINCE_CHOICES, DISTRICT_CHOICES, CATEGORY_CHOICES, Donor, CampSchedule, BloodStock

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

# Donor Registration form
class DonorForm(forms.ModelForm):
    bloodbank = forms.ModelChoiceField(
        queryset=BloodBankRegistration.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = Donor
        fields = ['name', 'profile_picture', 'blood_group', 'address', 'mobile', 'bloodbank']

class CampScheduleForm(forms.ModelForm):
    class Meta:
        model = CampSchedule
        fields = ['bloodbank', 'province', 'district', 'location', 'schedule_date', 'start_time', 'end_time', 'description']
        widgets = {
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BloodStockForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = ['blood_group', 'units']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'units': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

# Blood Bank Registration form
class BloodBankRegistrationForm(forms.ModelForm):
    # Section 1
    province = forms.ChoiceField(choices=PROVINCE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    district = forms.ChoiceField(choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    blood_bank_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    parent_hospital_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    short_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    contact_person = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contact_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pincode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    # Section 2
    donor_voluntary = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donor_replacement = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donor_directed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donor_autologous = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donor_family = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donor_replacement_external = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donation_leucapheresis = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donation_plasmapheresis = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donation_plateletpheresis = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    donation_whole_blood = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BloodBankRegistration
        fields = [
            'province', 'district', 'city', 'blood_bank_name', 'parent_hospital_name', 'short_name', 'category',
            'contact_person', 'email', 'contact_no', 'address', 'pincode', 'latitude', 'longitude',
            'donor_voluntary', 'donor_replacement', 'donor_directed', 'donor_autologous', 'donor_family', 'donor_replacement_external',
            'donation_leucapheresis', 'donation_plasmapheresis', 'donation_plateletpheresis', 'donation_whole_blood',
            'remark', 'username', 'password'
        ]
