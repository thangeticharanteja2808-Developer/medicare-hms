from django.contrib import admin
from .models import Patient, VisitRecord, Prescription, Appointment


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1
    fields = ['drug_name', 'dosage', 'frequency', 'duration', 'instructions']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['mrn', 'full_name', 'age', 'gender', 'blood_group', 'phone', 'status', 'created_at']
    list_filter = ['status', 'gender', 'blood_group']
    search_fields = ['first_name', 'last_name', 'mrn', 'phone', 'email']
    readonly_fields = ['mrn', 'created_at', 'updated_at']
    fieldsets = (
        ('Identity', {'fields': ('mrn', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'photo', 'status')}),
        ('Contact', {'fields': ('phone', 'email', 'address', 'city', 'state', 'pincode')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')}),
        ('Medical History', {'fields': ('allergies', 'chronic_conditions', 'current_medications', 'past_surgical_history', 'family_history')}),
        ('Insurance', {'fields': ('insurance_provider', 'insurance_policy_number', 'insurance_expiry')}),
        ('Notes & Timestamps', {'fields': ('notes', 'created_at', 'updated_at')}),
    )


@admin.register(VisitRecord)
class VisitRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'visit_date', 'visit_time', 'doctor', 'department', 'visit_type', 'diagnosis', 'status']
    list_filter = ['department', 'visit_type', 'status', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis', 'doctor']
    inlines = [PrescriptionInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'appointment_date', 'appointment_time', 'doctor', 'department', 'appointment_type', 'priority', 'status']
    list_filter = ['status', 'department', 'priority', 'appointment_type']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
