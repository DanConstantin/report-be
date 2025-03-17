from rest_framework import serializers

from preciseMed.models import Booking


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AddPatientSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    city = serializers.CharField()
    telephone = serializers.CharField(allow_null=True, allow_blank=True, )
    dateOfBirth = serializers.DateField(allow_null=True, required=False)
    allergies = serializers.CharField(allow_null=True, allow_blank=True, )
    medications = serializers.CharField(allow_null=True, allow_blank=True, )
    hasInsurance = serializers.BooleanField(default=False)
    previousConditions = serializers.CharField(allow_null=True, allow_blank=True,)

class AddBookingSerializer(serializers.Serializer):
    requestDescription = serializers.CharField()
    date = serializers.DateField()
    time = serializers.TimeField()


class DoctorUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    city = serializers.CharField(allow_null=True, allow_blank=True,)
    telephone = serializers.CharField(allow_null=True, allow_blank=True,)
    specialization = serializers.CharField()


class PatientUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    city = serializers.CharField(allow_null=True, allow_blank=True,)
    telephone = serializers.CharField(allow_null=True, allow_blank=True,)
    dateOfBirth = serializers.DateField(allow_null=True, required=False)
    allergies = serializers.CharField(allow_null=True, allow_blank=True,)
    medications = serializers.CharField(allow_null=True, allow_blank=True,)


class PatientSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    city = serializers.CharField()
    telephone = serializers.CharField()
    dateOfBirth = serializers.DateField()
    hasInsurance = serializers.BooleanField()
    allergies = serializers.CharField()
    medications = serializers.CharField()
    previousConditions = serializers.CharField()


class DoctorSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    city = serializers.CharField()
    telephone = serializers.CharField()
    specialization = serializers.CharField()

class BookingSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            'id',
            'timestamp',
            'patient',
            'requestDescription',
            'diagnosisDescription',
            'patient_full_name',
            'doctor',
            'mriUploaded',
            'aiPrediction'
        )

    def get_patient_full_name(self, obj):
        return obj.patient.get_full_name()

    def get_doctor(self, obj):
        if 'doctor' in self.context:
            doctor_serializer = DoctorSerializer(self.context['doctor'])
            return doctor_serializer.data

class DoctorBookingSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            'id',
            'timestamp',
            'patient',
            'requestDescription',
            'diagnosisDescription',
            'aiPrediction',
            'mriUploaded'
        )

    def get_patient(self, obj):
        patient_serializer = PatientSerializer(obj.patient)
        return patient_serializer.data