#!/usr/bin/env python3
"""
MediCare HMS — One-Click Setup & Run Script
Run: python setup_and_run.py
"""
import subprocess, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))

def run(cmd, **kw):
    print(f"\n▶ {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=BASE, **kw)
    if r.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(1)
    return r

def main():
    print("=" * 60)
    print("  🏥 MediCare HMS — Setup & Launch")
    print("=" * 60)

    # 1. Install dependencies
    print("\n📦 Installing dependencies...")
    run(f"{sys.executable} -m pip install -r requirements.txt --quiet")

    # 2. Migrations
    print("\n🗄️ Setting up database...")
    run(f"{sys.executable} manage.py makemigrations --noinput")
    run(f"{sys.executable} manage.py migrate --noinput")

    # 3. Create superuser
    print("\n👤 Creating admin superuser...")
    create_super = """
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@medicare.com', 'admin123')
    print('  ✅ Superuser created: admin / admin123')
else:
    print('  ℹ️  Superuser already exists')
"""
    run(f'{sys.executable} -c "{create_super}"')

    # 4. Load demo data
    print("\n🌱 Loading demo patient data...")
    load_demo = """
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_project.settings')
django.setup()
from patients.models import Patient, VisitRecord, Prescription, Appointment
from datetime import date, time, timedelta

if Patient.objects.count() == 0:
    p1 = Patient.objects.create(first_name='Aisha', last_name='Rahman', date_of_birth=date(1985,3,14), gender='Female', blood_group='B+', phone='9876543210', email='aisha.r@email.com', address='12 MG Road', city='Hyderabad', pincode='500001', emergency_contact_name='Ahmed Rahman', emergency_contact_phone='9876543211', allergies='Penicillin', chronic_conditions='Hypertension, Diabetes Type 2', insurance_provider='Star Health', insurance_policy_number='POL123456')
    p2 = Patient.objects.create(first_name='Ravi', last_name='Kumar', date_of_birth=date(1972,7,22), gender='Male', blood_group='O+', phone='9123456789', email='ravi.k@email.com', address='45 Banjara Hills', city='Hyderabad', pincode='500034', allergies='Sulfa drugs', chronic_conditions='Asthma', insurance_provider='HDFC ERGO', insurance_policy_number='POL789012')
    p3 = Patient.objects.create(first_name='Priya', last_name='Singh', date_of_birth=date(1995,11,8), gender='Female', blood_group='A-', phone='9988776655', email='priya.s@email.com', address='78 Jubilee Hills', city='Hyderabad', pincode='500096', allergies='None', chronic_conditions='Migraine', insurance_provider='Max Bupa', insurance_policy_number='POL345678')
    p4 = Patient.objects.create(first_name='Mohammed', last_name='Ali', date_of_birth=date(1960,5,10), gender='Male', blood_group='AB+', phone='9700001111', address='23 Old City', city='Hyderabad', allergies='Aspirin', chronic_conditions='Coronary Artery Disease, Hypertension')
    p5 = Patient.objects.create(first_name='Sunita', last_name='Devi', date_of_birth=date(2001,9,3), gender='Female', blood_group='A+', phone='9800002222', address='Secunderabad', city='Hyderabad', allergies='None', chronic_conditions='Hypothyroidism')

    v1 = VisitRecord.objects.create(patient=p1, visit_date=date.today()-timedelta(days=14), visit_time=time(10,30), doctor='Dr. Kavita Sharma', department='Cardiology', visit_type='Follow-up', blood_pressure='140/90', pulse_rate='82', temperature='98.6', spo2='97', weight='68', height='162', bmi='25.9', respiratory_rate='18', chief_complaint='Chest discomfort, shortness of breath', history_of_illness='Patient reports mild chest pain radiating to left arm, occasional dizziness for past 1 week.', physical_examination='Heart sounds S1 S2 normal, mild bilateral pedal edema present.', diagnosis='Hypertensive heart disease - stable', treatment_plan='Continue Amlodipine 5mg, added Furosemide 20mg for edema management.', investigations_ordered='ECG, CBC, Lipid profile', follow_up_instructions='Review in 2 weeks with lab reports', additional_notes='Patient counseled on low-sodium diet and regular BP monitoring.', status='Completed')
    Prescription.objects.create(visit=v1, drug_name='Amlodipine', dosage='5mg', frequency='Once daily at night', duration='30 days')
    Prescription.objects.create(visit=v1, drug_name='Furosemide', dosage='20mg', frequency='Morning', duration='14 days')
    Prescription.objects.create(visit=v1, drug_name='Aspirin', dosage='75mg', frequency='Once daily after food', duration='Ongoing')

    v2 = VisitRecord.objects.create(patient=p2, visit_date=date.today()-timedelta(days=7), visit_time=time(14,0), doctor='Dr. Sanjay Mehta', department='Pulmonology', visit_type='Emergency', blood_pressure='120/80', pulse_rate='96', temperature='99.1', spo2='93', weight='75', height='170', bmi='26.0', respiratory_rate='22', chief_complaint='Acute wheezing and breathlessness', history_of_illness='Sudden onset wheezing after dust exposure at workplace.', physical_examination='Bilateral expiratory wheeze, prolonged expiration phase.', diagnosis='Acute exacerbation of bronchial asthma', treatment_plan='Nebulization with Salbutamol + Ipratropium. Short course oral steroids.', investigations_ordered='Spirometry, Chest X-Ray, ABG', follow_up_instructions='Follow up in 1 week. Avoid dust, smoke, cold air.', status='Completed')
    Prescription.objects.create(visit=v2, drug_name='Salbutamol Inhaler', dosage='2 puffs', frequency='As needed (max 4 hourly)', duration='PRN')
    Prescription.objects.create(visit=v2, drug_name='Budesonide Inhaler', dosage='200mcg', frequency='Twice daily', duration='4 weeks')

    today = date.today()
    Appointment.objects.create(patient=p1, appointment_date=today+timedelta(days=3), appointment_time=time(10,30), doctor='Dr. Kavita Sharma', department='Cardiology', appointment_type='Follow-up', duration_minutes='30', reason='Blood pressure review and lipid profile discussion', priority='Normal', status='Confirmed')
    Appointment.objects.create(patient=p2, appointment_date=today+timedelta(days=5), appointment_time=time(11,0), doctor='Dr. Sanjay Mehta', department='Pulmonology', appointment_type='Follow-up', duration_minutes='20', reason='Spirometry review and inhaler technique check', priority='Normal', status='Pending')
    Appointment.objects.create(patient=p3, appointment_date=today+timedelta(days=2), appointment_time=time(15,30), doctor='Dr. Ananya Rao', department='Neurology', appointment_type='New Consultation', duration_minutes='45', reason='Migraine follow-up and MRI brain review', priority='High', status='Pending', notes='Patient to bring MRI CD and previous prescription')
    Appointment.objects.create(patient=p4, appointment_date=today, appointment_time=time(9,0), doctor='Dr. Kavita Sharma', department='Cardiology', appointment_type='Follow-up', duration_minutes='30', reason='Post angioplasty follow-up', priority='Urgent', status='Confirmed')

    print('  ✅ Demo data loaded: 5 patients, 2 visits, 4 appointments')
else:
    print(f'  ℹ️  Demo data already present ({Patient.objects.count()} patients)')
"""
    run(f'{sys.executable} -c "{load_demo}"')

    # 5. Collect static
    run(f"{sys.executable} manage.py collectstatic --noinput --quiet")

    print("\n" + "=" * 60)
    print("  ✅ MediCare HMS is ready!")
    print("=" * 60)
    print("\n  🌐 Open in browser: http://127.0.0.1:8000")
    print("  🏥 HMS Portal:       http://127.0.0.1:8000/dashboard/")
    print("  ⚙️  Admin Panel:      http://127.0.0.1:8000/admin/")
    print("  🔌 REST API:         http://127.0.0.1:8000/api/")
    print("\n  👤 Admin login:  admin / admin123")
    print("\n  Press Ctrl+C to stop the server")
    print("=" * 60)

    # 6. Run server
    run(f"{sys.executable} manage.py runserver 8000")

if __name__ == "__main__":
    main()
