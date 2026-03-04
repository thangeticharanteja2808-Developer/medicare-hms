from rest_framework import serializers
from .models import Patient, VisitRecord, Prescription, Appointment


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'drug_name', 'dosage', 'frequency', 'duration', 'instructions']


class PatientListSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    visit_count = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'mrn', 'first_name', 'last_name', 'full_name', 'date_of_birth',
                  'age', 'gender', 'blood_group', 'phone', 'email', 'status',
                  'chronic_conditions', 'allergies', 'created_at', 'visit_count']

    def get_visit_count(self, obj):
        return obj.visits.count()


class PatientDetailSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = '__all__'


class VisitListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    patient_mrn = serializers.SerializerMethodField()
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = VisitRecord
        fields = ['id', 'patient', 'patient_name', 'patient_mrn', 'visit_date', 'visit_time',
                  'doctor', 'department', 'visit_type', 'chief_complaint', 'diagnosis',
                  'status', 'prescriptions', 'created_at',
                  'blood_pressure', 'pulse_rate', 'temperature', 'spo2',
                  'weight', 'height', 'bmi', 'respiratory_rate']

    def get_patient_name(self, obj):
        return obj.patient.full_name

    def get_patient_mrn(self, obj):
        return obj.patient.mrn


class VisitDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    patient_mrn = serializers.SerializerMethodField()
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = VisitRecord
        fields = '__all__'

    def get_patient_name(self, obj):
        return obj.patient.full_name

    def get_patient_mrn(self, obj):
        return obj.patient.mrn


class VisitCreateSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, required=False)

    class Meta:
        model = VisitRecord
        fields = '__all__'

    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', [])
        visit = VisitRecord.objects.create(**validated_data)
        for presc in prescriptions_data:
            Prescription.objects.create(visit=visit, **presc)
        return visit

    def update(self, instance, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if prescriptions_data is not None:
            instance.prescriptions.all().delete()
            for presc in prescriptions_data:
                Prescription.objects.create(visit=instance, **presc)
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    patient_mrn = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_name(self, obj):
        return obj.patient.full_name

    def get_patient_mrn(self, obj):
        return obj.patient.mrn
