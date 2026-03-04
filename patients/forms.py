from django import forms
from django.forms import inlineformset_factory
from .models import Patient, VisitRecord, Appointment, Prescription, DEPARTMENT_CHOICES, DOCTOR_CHOICES

WIDGET_ATTRS = {'class': 'form-control'}
DATE_ATTRS = {'class': 'form-control', 'type': 'date'}
TIME_ATTRS = {'class': 'form-control', 'type': 'time'}
SELECT_ATTRS = {'class': 'form-select'}
TEXTAREA_ATTRS = {'class': 'form-control', 'rows': 3}


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['mrn', 'created_at', 'updated_at']
        widgets = {
            'first_name': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Last name'}),
            'date_of_birth': forms.DateInput(attrs=DATE_ATTRS),
            'gender': forms.Select(attrs=SELECT_ATTRS),
            'blood_group': forms.Select(attrs=SELECT_ATTRS),
            'phone': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '+91 XXXXX XXXXX'}),
            'email': forms.EmailInput(attrs={**WIDGET_ATTRS, 'placeholder': 'patient@email.com'}),
            'address': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 2, 'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'PIN Code'}),
            'emergency_contact_name': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Contact name'}),
            'emergency_contact_phone': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Contact phone'}),
            'emergency_contact_relation': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. Spouse, Parent'}),
            'allergies': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'e.g. Penicillin, Sulfa (write None if no allergies)'}),
            'chronic_conditions': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'e.g. Diabetes Type 2, Hypertension'}),
            'current_medications': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'List current medications'}),
            'past_surgical_history': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Any past surgeries'}),
            'family_history': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Relevant family medical history'}),
            'insurance_provider': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. Star Health'}),
            'insurance_policy_number': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Policy number'}),
            'insurance_expiry': forms.DateInput(attrs=DATE_ATTRS),
            'status': forms.Select(attrs=SELECT_ATTRS),
            'notes': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Additional notes'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class VisitRecordForm(forms.ModelForm):
    class Meta:
        model = VisitRecord
        exclude = ['created_at', 'updated_at']
        widgets = {
            'patient': forms.Select(attrs=SELECT_ATTRS),
            'visit_date': forms.DateInput(attrs=DATE_ATTRS),
            'visit_time': forms.TimeInput(attrs=TIME_ATTRS),
            'doctor': forms.Select(attrs=SELECT_ATTRS),
            'department': forms.Select(attrs=SELECT_ATTRS),
            'visit_type': forms.Select(attrs=SELECT_ATTRS),
            'blood_pressure': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '120/80'}),
            'pulse_rate': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '72'}),
            'temperature': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '98.6'}),
            'spo2': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '99'}),
            'weight': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '70'}),
            'height': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '170'}),
            'bmi': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '24.2'}),
            'respiratory_rate': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': '16'}),
            'chief_complaint': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Main reason for visit...'}),
            'history_of_illness': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Detailed history...'}),
            'physical_examination': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Examination findings...'}),
            'diagnosis': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Clinical diagnosis...', 'rows': 2}),
            'treatment_plan': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Treatment and medications...'}),
            'investigations_ordered': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Lab tests, imaging...'}),
            'follow_up_instructions': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 2, 'placeholder': 'e.g. Review after 2 weeks'}),
            'additional_notes': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Any additional notes...'}),
            'status': forms.Select(attrs=SELECT_ATTRS),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ['visit']
        widgets = {
            'drug_name': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Drug name'}),
            'dosage': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. 500mg'}),
            'frequency': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. Twice daily'}),
            'duration': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g. 5 days'}),
            'instructions': forms.TextInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Special instructions'}),
        }


PrescriptionFormSet = inlineformset_factory(
    VisitRecord, Prescription,
    form=PrescriptionForm,
    extra=2, can_delete=True, max_num=20
)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['created_at', 'updated_at']
        widgets = {
            'patient': forms.Select(attrs=SELECT_ATTRS),
            'appointment_date': forms.DateInput(attrs=DATE_ATTRS),
            'appointment_time': forms.TimeInput(attrs=TIME_ATTRS),
            'doctor': forms.Select(attrs=SELECT_ATTRS),
            'department': forms.Select(attrs=SELECT_ATTRS),
            'appointment_type': forms.Select(attrs=SELECT_ATTRS),
            'duration_minutes': forms.Select(attrs=SELECT_ATTRS),
            'reason': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 2, 'placeholder': 'Reason for appointment...'}),
            'priority': forms.Select(attrs=SELECT_ATTRS),
            'status': forms.Select(attrs=SELECT_ATTRS),
            'notes': forms.Textarea(attrs={**TEXTAREA_ATTRS, 'rows': 2, 'placeholder': 'Special instructions...'}),
        }
