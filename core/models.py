from django.db import models
from django.contrib.auth.hashers import make_password

class AboutRaktaSewa(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About RaktaSewa"
        verbose_name_plural = "About RaktaSewa"

    def __str__(self):
        return f"About RaktaSewa (updated {self.updated_at:%Y-%m-%d})"

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"

class MobileApp(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    download_link = models.URLField()

    def __str__(self):
        return self.name

# --- Blood Bank Registration ---

PROVINCE_CHOICES = [
    ('Province 1', 'Province 1'),
    ('Province 2', 'Province 2'),
    ('Bagmati', 'Bagmati (Province 3)'),
    ('Gandaki', 'Gandaki (Province 4)'),
    ('Lumbini', 'Lumbini (Province 5)'),
    ('Karnali', 'Karnali (Province 6)'),
    ('Sudurpashchim', 'Sudurpashchim (Province 7)'),
]

# List of all 77 districts of Nepal
DISTRICT_CHOICES = [
    ('Achham', 'Achham'), ('Arghakhanchi', 'Arghakhanchi'), ('Baglung', 'Baglung'), ('Baitadi', 'Baitadi'),
    ('Bajhang', 'Bajhang'), ('Bajura', 'Bajura'), ('Banke', 'Banke'), ('Bara', 'Bara'), ('Bardiya', 'Bardiya'),
    ('Bhaktapur', 'Bhaktapur'), ('Bhojpur', 'Bhojpur'), ('Chitwan', 'Chitwan'), ('Dadeldhura', 'Dadeldhura'),
    ('Dailekh', 'Dailekh'), ('Dang', 'Dang'), ('Darchula', 'Darchula'), ('Dhading', 'Dhading'),
    ('Dhankuta', 'Dhankuta'), ('Dhanusa', 'Dhanusa'), ('Dolakha', 'Dolakha'), ('Dolpa', 'Dolpa'),
    ('Doti', 'Doti'), ('Gorkha', 'Gorkha'), ('Gulmi', 'Gulmi'), ('Humla', 'Humla'), ('Ilam', 'Ilam'),
    ('Jajarkot', 'Jajarkot'), ('Jhapa', 'Jhapa'), ('Jumla', 'Jumla'), ('Kailali', 'Kailali'),
    ('Kalikot', 'Kalikot'), ('Kanchanpur', 'Kanchanpur'), ('Kapilvastu', 'Kapilvastu'), ('Kaski', 'Kaski'),
    ('Kathmandu', 'Kathmandu'), ('Kavrepalanchok', 'Kavrepalanchok'), ('Khotang', 'Khotang'),
    ('Lalitpur', 'Lalitpur'), ('Lamjung', 'Lamjung'), ('Mahottari', 'Mahottari'), ('Makwanpur', 'Makwanpur'),
    ('Manang', 'Manang'), ('Morang', 'Morang'), ('Mugu', 'Mugu'), ('Mustang', 'Mustang'), ('Myagdi', 'Myagdi'),
    ('Nawalparasi East', 'Nawalparasi East'), ('Nawalparasi West', 'Nawalparasi West'), ('Nuwakot', 'Nuwakot'),
    ('Okhaldhunga', 'Okhaldhunga'), ('Palpa', 'Palpa'), ('Panchthar', 'Panchthar'), ('Parbat', 'Parbat'),
    ('Parsa', 'Parsa'), ('Pyuthan', 'Pyuthan'), ('Ramechhap', 'Ramechhap'), ('Rasuwa', 'Rasuwa'),
    ('Rautahat', 'Rautahat'), ('Rolpa', 'Rolpa'), ('Rukum East', 'Rukum East'), ('Rukum West', 'Rukum West'),
    ('Rupandehi', 'Rupandehi'), ('Salyan', 'Salyan'), ('Sankhuwasabha', 'Sankhuwasabha'), ('Saptari', 'Saptari'),
    ('Sarlahi', 'Sarlahi'), ('Sindhuli', 'Sindhuli'), ('Sindhupalchok', 'Sindhupalchok'), ('Siraha', 'Siraha'),
    ('Solukhumbu', 'Solukhumbu'), ('Sunsari', 'Sunsari'), ('Surkhet', 'Surkhet'), ('Syangja', 'Syangja'),
    ('Tanahun', 'Tanahun'), ('Taplejung', 'Taplejung'), ('Terhathum', 'Terhathum'), ('Udayapur', 'Udayapur'),
]

CATEGORY_CHOICES = [
    ('Government', 'Government'),
    ('Private', 'Private'),
    ('Community', 'Community'),
]

DONOR_TYPE_CHOICES = [
    ('voluntary', 'Voluntary'),
    ('replacement', 'Replacement'),
    ('directed', 'Directed'),
    ('autologous', 'Autologous'),
    ('family', 'Family'),
    ('replacement_external', 'Replacement External'),
]

DONATION_TYPE_CHOICES = [
    ('leucapheresis', 'Leucapheresis'),
    ('plasmapheresis', 'Plasmapheresis'),
    ('plateletpheresis', 'Plateletpheresis'),
    ('whole_blood', 'Whole Blood'),
]

class BloodBankRegistration(models.Model):
    # Section 1: Blood Bank Information
    province = models.CharField(max_length=30, choices=PROVINCE_CHOICES)
    district = models.CharField(max_length=30, choices=DISTRICT_CHOICES)
    city = models.CharField(max_length=100)
    blood_bank_name = models.CharField(max_length=200)
    parent_hospital_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Section 2: Donation Information
    donor_voluntary = models.BooleanField(default=False)
    donor_replacement = models.BooleanField(default=False)
    donor_directed = models.BooleanField(default=False)
    donor_autologous = models.BooleanField(default=False)
    donor_family = models.BooleanField(default=False)
    donor_replacement_external = models.BooleanField(default=False)

    donation_leucapheresis = models.BooleanField(default=False)
    donation_plasmapheresis = models.BooleanField(default=False)
    donation_plateletpheresis = models.BooleanField(default=False)
    donation_whole_blood = models.BooleanField(default=False)

    remark = models.TextField(blank=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # hashed
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash password if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.blood_bank_name} ({self.city}, {self.district})"

class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='donor_profiles/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    bloodbank = models.ForeignKey(
        BloodBankRegistration,
        to_field='username',
        db_column='bloodbank',
        on_delete=models.CASCADE,
        related_name='donors'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class CampSchedule(models.Model):
    bloodbank = models.ForeignKey(BloodBankRegistration, on_delete=models.CASCADE, related_name='camps')
    province = models.CharField(max_length=30, choices=PROVINCE_CHOICES)
    district = models.CharField(max_length=30, choices=DISTRICT_CHOICES)
    location = models.CharField(max_length=255)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Camp at {self.location} on {self.schedule_date}"

class BloodStock(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    bloodbank = models.ForeignKey(BloodBankRegistration, on_delete=models.CASCADE, related_name='blood_stock')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bloodbank', 'blood_group')

    def __str__(self):
        return f"{self.blood_group}: {self.units} units at {self.bloodbank.blood_bank_name}"

    def save(self, *args, **kwargs):
        # Ensure only one record exists per blood group per blood bank
        BloodStock.objects.filter(
            bloodbank=self.bloodbank,
            blood_group=self.blood_group
        ).exclude(id=self.id).delete()
        super().save(*args, **kwargs)