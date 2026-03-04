from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date

from .models import Patient, VisitRecord, Appointment, Prescription
from .serializers import (
    PatientListSerializer, PatientDetailSerializer,
    VisitListSerializer, VisitDetailSerializer, VisitCreateSerializer,
    AppointmentSerializer, PrescriptionSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'mrn', 'phone', 'email']
    ordering_fields = ['created_at', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.action in ['list']:
            return PatientListSerializer
        return PatientDetailSerializer

    def get_queryset(self):
        qs = Patient.objects.all()
        status_filter = self.request.query_params.get('status')
        gender = self.request.query_params.get('gender')
        blood = self.request.query_params.get('blood_group')
        if status_filter:
            qs = qs.filter(status=status_filter)
        if gender:
            qs = qs.filter(gender=gender)
        if blood:
            qs = qs.filter(blood_group=blood)
        return qs

    @action(detail=True, methods=['get'])
    def visits(self, request, pk=None):
        patient = self.get_object()
        visits = patient.visits.all()
        serializer = VisitListSerializer(visits, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        patient = self.get_object()
        appointments = patient.appointments.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        patient = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['Active', 'Inactive', 'Discharged']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        patient.status = new_status
        patient.save()
        return Response({'status': 'updated', 'new_status': new_status})


class VisitViewSet(viewsets.ModelViewSet):
    queryset = VisitRecord.objects.select_related('patient').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis', 'doctor', 'department']
    ordering_fields = ['visit_date', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return VisitCreateSerializer
        if self.action == 'retrieve':
            return VisitDetailSerializer
        return VisitListSerializer

    def get_queryset(self):
        qs = VisitRecord.objects.select_related('patient').prefetch_related('prescriptions')
        patient_id = self.request.query_params.get('patient')
        department = self.request.query_params.get('department')
        doctor = self.request.query_params.get('doctor')
        visit_status = self.request.query_params.get('status')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if department:
            qs = qs.filter(department=department)
        if doctor:
            qs = qs.filter(doctor=doctor)
        if visit_status:
            qs = qs.filter(status=visit_status)
        if date_from:
            qs = qs.filter(visit_date__gte=date_from)
        if date_to:
            qs = qs.filter(visit_date__lte=date_to)
        return qs

    @action(detail=True, methods=['post'])
    def add_prescription(self, request, pk=None):
        visit = self.get_object()
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient').all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor', 'department', 'reason']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at']

    def get_queryset(self):
        qs = Appointment.objects.select_related('patient').all()
        appt_status = self.request.query_params.get('status')
        patient_id = self.request.query_params.get('patient')
        doctor = self.request.query_params.get('doctor')
        department = self.request.query_params.get('department')
        date_filter = self.request.query_params.get('date')
        today_only = self.request.query_params.get('today')
        upcoming = self.request.query_params.get('upcoming')

        if appt_status:
            qs = qs.filter(status=appt_status)
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if doctor:
            qs = qs.filter(doctor=doctor)
        if department:
            qs = qs.filter(department=department)
        if date_filter:
            qs = qs.filter(appointment_date=date_filter)
        if today_only:
            qs = qs.filter(appointment_date=date.today())
        if upcoming:
            qs = qs.filter(appointment_date__gte=date.today())
        return qs

    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        appt = self.get_object()
        appt.status = 'Confirmed'
        appt.save()
        return Response({'status': 'confirmed'})

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        appt.status = 'Cancelled'
        appt.save()
        return Response({'status': 'cancelled'})

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        appt = self.get_object()
        appt.status = 'Completed'
        appt.save()
        return Response({'status': 'completed'})


from rest_framework.decorators import api_view
from rest_framework.response import Response as DRFResponse


@api_view(['GET'])
def dashboard_stats(request):
    today = date.today()
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status='Active').count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    pending_appointments = Appointment.objects.filter(status='Pending').count()
    confirmed_appointments = Appointment.objects.filter(status='Confirmed').count()
    total_visits = VisitRecord.objects.count()
    today_visits = VisitRecord.objects.filter(visit_date=today).count()

    recent_patients = PatientListSerializer(
        Patient.objects.order_by('-created_at')[:5], many=True
    ).data
    today_appts = AppointmentSerializer(
        Appointment.objects.filter(appointment_date=today).order_by('appointment_time'), many=True
    ).data

    return DRFResponse({
        'total_patients': total_patients,
        'active_patients': active_patients,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'total_visits': total_visits,
        'today_visits': today_visits,
        'recent_patients': recent_patients,
        'today_appointments_list': today_appts,
    })
