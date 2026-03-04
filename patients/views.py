from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date, datetime
from .models import Patient, VisitRecord, Appointment, Prescription, DEPARTMENT_CHOICES, DOCTOR_CHOICES
from .forms import PatientForm, VisitRecordForm, AppointmentForm, PrescriptionFormSet


def dashboard(request):
    today = date.today()
    ctx = {
        'total_patients': Patient.objects.count(),
        'active_patients': Patient.objects.filter(status='Active').count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'pending_appointments': Appointment.objects.filter(status='Pending').count(),
        'total_visits': VisitRecord.objects.count(),
        'today_visits': VisitRecord.objects.filter(visit_date=today).count(),
        'recent_patients': Patient.objects.order_by('-created_at')[:6],
        'today_appts': Appointment.objects.filter(appointment_date=today).order_by('appointment_time'),
        'upcoming_appts': Appointment.objects.filter(
            appointment_date__gte=today, status__in=['Pending','Confirmed']
        ).order_by('appointment_date', 'appointment_time')[:5],
        'page': 'dashboard',
    }
    return render(request, 'patients/dashboard.html', ctx)


# ── PATIENTS ──────────────────────────────────────────────────────────────────
def patient_list(request):
    qs = Patient.objects.all()
    q = request.GET.get('q', '')
    status_f = request.GET.get('status', '')
    gender_f = request.GET.get('gender', '')
    if q:
        qs = qs.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q)|
                       Q(mrn__icontains=q)|Q(phone__icontains=q)|Q(email__icontains=q))
    if status_f:
        qs = qs.filter(status=status_f)
    if gender_f:
        qs = qs.filter(gender=gender_f)
    return render(request, 'patients/patient_list.html', {
        'patients': qs, 'q': q, 'status_f': status_f, 'gender_f': gender_f,
        'total': qs.count(), 'page': 'patients',
    })


def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} registered successfully! MRN: {patient.mrn}')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form, 'page': 'patients', 'action': 'Register'})


def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient record updated successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {
        'form': form, 'patient': patient, 'page': 'patients', 'action': 'Edit'
    })


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    visits = patient.visits.prefetch_related('prescriptions').all()
    appointments = patient.appointments.order_by('-appointment_date')
    return render(request, 'patients/patient_detail.html', {
        'patient': patient, 'visits': visits, 'appointments': appointments,
        'page': 'patients',
    })


def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.full_name
        patient.delete()
        messages.success(request, f'Patient record for {name} deleted.')
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient, 'page': 'patients'})


# ── VISITS ────────────────────────────────────────────────────────────────────
def visit_list(request):
    qs = VisitRecord.objects.select_related('patient').prefetch_related('prescriptions')
    q = request.GET.get('q', '')
    patient_id = request.GET.get('patient', '')
    dept = request.GET.get('department', '')
    if q:
        qs = qs.filter(Q(patient__first_name__icontains=q)|Q(patient__last_name__icontains=q)|
                       Q(diagnosis__icontains=q)|Q(doctor__icontains=q))
    if patient_id:
        qs = qs.filter(patient_id=patient_id)
    if dept:
        qs = qs.filter(department=dept)
    return render(request, 'patients/visit_list.html', {
        'visits': qs, 'q': q, 'patient_id': patient_id, 'dept': dept,
        'patients': Patient.objects.all(), 'departments': DEPARTMENT_CHOICES,
        'total': qs.count(), 'page': 'visits',
    })


def visit_add(request):
    patient_id = request.GET.get('patient') or request.POST.get('patient')
    initial = {}
    if patient_id:
        initial['patient'] = patient_id
    if request.method == 'POST':
        form = VisitRecordForm(request.POST)
        formset = PrescriptionFormSet(request.POST, prefix='presc')
        if form.is_valid() and formset.is_valid():
            visit = form.save()
            prescriptions = formset.save(commit=False)
            for presc in prescriptions:
                presc.visit = visit
                presc.save()
            messages.success(request, f'Visit record saved successfully.')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitRecordForm(initial=initial)
        formset = PrescriptionFormSet(prefix='presc')
    return render(request, 'patients/visit_form.html', {
        'form': form, 'formset': formset, 'page': 'visits', 'action': 'New',
        'patients': Patient.objects.filter(status='Active'),
    })


def visit_detail(request, pk):
    visit = get_object_or_404(VisitRecord, pk=pk)
    return render(request, 'patients/visit_detail.html', {'visit': visit, 'page': 'visits'})


def visit_edit(request, pk):
    visit = get_object_or_404(VisitRecord, pk=pk)
    if request.method == 'POST':
        form = VisitRecordForm(request.POST, instance=visit)
        formset = PrescriptionFormSet(request.POST, instance=visit, prefix='presc')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Visit record updated.')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitRecordForm(instance=visit)
        formset = PrescriptionFormSet(instance=visit, prefix='presc')
    return render(request, 'patients/visit_form.html', {
        'form': form, 'formset': formset, 'visit': visit,
        'page': 'visits', 'action': 'Edit',
        'patients': Patient.objects.filter(status='Active'),
    })


# ── APPOINTMENTS ──────────────────────────────────────────────────────────────
def appointment_list(request):
    qs = Appointment.objects.select_related('patient').all()
    q = request.GET.get('q', '')
    status_f = request.GET.get('status', '')
    dept = request.GET.get('department', '')
    date_f = request.GET.get('date', '')
    if q:
        qs = qs.filter(Q(patient__first_name__icontains=q)|Q(patient__last_name__icontains=q)|
                       Q(doctor__icontains=q)|Q(reason__icontains=q))
    if status_f:
        qs = qs.filter(status=status_f)
    if dept:
        qs = qs.filter(department=dept)
    if date_f:
        qs = qs.filter(appointment_date=date_f)
    return render(request, 'patients/appointment_list.html', {
        'appointments': qs, 'q': q, 'status_f': status_f, 'dept': dept, 'date_f': date_f,
        'departments': DEPARTMENT_CHOICES, 'total': qs.count(), 'page': 'appointments',
    })


def appointment_add(request):
    patient_id = request.GET.get('patient') or request.POST.get('patient')
    initial = {}
    if patient_id:
        initial['patient'] = patient_id
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            messages.success(request, f'Appointment scheduled for {appt.patient.full_name}.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(initial=initial)
    return render(request, 'patients/appointment_form.html', {
        'form': form, 'page': 'appointments', 'action': 'Schedule',
        'patients': Patient.objects.filter(status='Active'),
    })


def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appt)
    return render(request, 'patients/appointment_form.html', {
        'form': form, 'appt': appt, 'page': 'appointments', 'action': 'Edit',
        'patients': Patient.objects.filter(status='Active'),
    })


def appointment_status(request, pk, new_status):
    appt = get_object_or_404(Appointment, pk=pk)
    valid = ['Confirmed', 'Cancelled', 'Completed', 'No-Show']
    if new_status in valid:
        appt.status = new_status
        appt.save()
        messages.success(request, f'Appointment {new_status.lower()}.')
    return redirect(request.META.get('HTTP_REFERER', 'appointment_list'))
