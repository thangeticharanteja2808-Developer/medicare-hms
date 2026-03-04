from django.db import models
from django.utils import timezone
import uuid


def generate_mrn():
    """Generate unique Medical Record Number"""
    year = timezone.now().year
    count = Patient.objects.filter(created_at__year=year).count() + 1
    return f"MRN-{year}-{str(count).zfill(4)}"


class Patient(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    BLOOD_CHOICES = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                     ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('Unknown', 'Unknown')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive'), ('Discharged', 'Discharged')]

    # Identity
    mrn = models.CharField(max_length=30, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=10, choices=BLOOD_CHOICES, blank=True)
    photo = models.ImageField(upload_to='patient_photos/', null=True, blank=True)

    # Contact
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    # Emergency
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=100, blank=True)

    # Medical
    allergies = models.TextField(blank=True, default='None')
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    past_surgical_history = models.TextField(blank=True)
    family_history = models.TextField(blank=True)

    # Insurance
    insurance_provider = models.CharField(max_length=200, blank=True)
    insurance_policy_number = models.CharField(max_length=100, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)

    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.mrn:
            self.mrn = generate_mrn()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.mrn})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


DEPARTMENT_CHOICES = [
    ('Cardiology', 'Cardiology'), ('Pulmonology', 'Pulmonology'),
    ('Neurology', 'Neurology'), ('Orthopedics', 'Orthopedics'),
    ('General Medicine', 'General Medicine'), ('Pediatrics', 'Pediatrics'),
    ('Gynecology', 'Gynecology'), ('Dermatology', 'Dermatology'),
    ('ENT', 'ENT'), ('Ophthalmology', 'Ophthalmology'),
    ('Oncology', 'Oncology'), ('Urology', 'Urology'),
    ('Psychiatry', 'Psychiatry'), ('Endocrinology', 'Endocrinology'),
    ('Gastroenterology', 'Gastroenterology'), ('Nephrology', 'Nephrology'),
    ('Rheumatology', 'Rheumatology'), ('Emergency', 'Emergency'),
]

DOCTOR_CHOICES = [
    ('Dr. Kavita Sharma', 'Dr. Kavita Sharma'),
    ('Dr. Sanjay Mehta', 'Dr. Sanjay Mehta'),
    ('Dr. Ananya Rao', 'Dr. Ananya Rao'),
    ('Dr. Rajesh Patel', 'Dr. Rajesh Patel'),
    ('Dr. Meera Nair', 'Dr. Meera Nair'),
    ('Dr. Arun Verma', 'Dr. Arun Verma'),
    ('Dr. Priya Reddy', 'Dr. Priya Reddy'),
    ('Dr. Suresh Kumar', 'Dr. Suresh Kumar'),
]


class VisitRecord(models.Model):
    VISIT_TYPE_CHOICES = [
        ('Regular', 'Regular'), ('Follow-up', 'Follow-up'),
        ('Emergency', 'Emergency'), ('Routine Check-up', 'Routine Check-up'),
        ('Pre-operative', 'Pre-operative'), ('Post-operative', 'Post-operative'),
    ]
    STATUS_CHOICES = [('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(default=timezone.now)
    visit_time = models.TimeField()
    doctor = models.CharField(max_length=200, choices=DOCTOR_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    visit_type = models.CharField(max_length=50, choices=VISIT_TYPE_CHOICES, default='Regular')

    # Vitals
    blood_pressure = models.CharField(max_length=20, blank=True)
    pulse_rate = models.CharField(max_length=20, blank=True)
    temperature = models.CharField(max_length=20, blank=True)
    spo2 = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=20, blank=True)
    height = models.CharField(max_length=20, blank=True)
    bmi = models.CharField(max_length=20, blank=True)
    respiratory_rate = models.CharField(max_length=20, blank=True)

    # Clinical Notes
    chief_complaint = models.TextField()
    history_of_illness = models.TextField(blank=True)
    physical_examination = models.TextField(blank=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField(blank=True)
    investigations_ordered = models.TextField(blank=True)
    follow_up_instructions = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-visit_date', '-visit_time']

    def __str__(self):
        return f"Visit: {self.patient.full_name} on {self.visit_date} ({self.department})"


class Prescription(models.Model):
    visit = models.ForeignKey(VisitRecord, on_delete=models.CASCADE, related_name='prescriptions')
    drug_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.drug_name} {self.dosage} - {self.frequency}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'), ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('No-Show', 'No-Show'),
    ]
    TYPE_CHOICES = [
        ('New Consultation', 'New Consultation'), ('Follow-up', 'Follow-up'),
        ('Emergency', 'Emergency'), ('Procedure', 'Procedure'), ('Lab Review', 'Lab Review'),
    ]
    PRIORITY_CHOICES = [('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High'), ('Urgent', 'Urgent')]
    DURATION_CHOICES = [('15', '15 min'), ('20', '20 min'), ('30', '30 min'),
                        ('45', '45 min'), ('60', '60 min'), ('90', '90 min')]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor = models.CharField(max_length=200, choices=DOCTOR_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    appointment_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='New Consultation')
    duration_minutes = models.CharField(max_length=10, choices=DURATION_CHOICES, default='30')
    reason = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"Appt: {self.patient.full_name} — {self.appointment_date} {self.appointment_time}"
