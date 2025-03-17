from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta, datetime, date, time
from django.utils import timezone
import torch
from PIL import Image
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn

from .models import CustomUser, UserRelationship, Booking, Patient, Doctor
from .permissions import MedicPermission, PatientPermission, GuestPermission
from .serializers import AddPatientSerializer, PatientSerializer, DoctorUpdateSerializer, DoctorSerializer, \
    PatientUpdateSerializer, BookingSerializer, DoctorBookingSerializer, AddBookingSerializer

# Create your views here.
User = get_user_model()


def serve_index(request):
    with open('static/index.html', 'r') as f:
        return HttpResponse(f.read())

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['name'] = user.get_full_name()
        token['role'] = "".join(user.groups.values_list('name', flat=True))
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@permission_classes([GuestPermission])
class HealthCheckView(APIView):
    def get(self, request):
        return Response({'status': 'OK', 'time': timezone.now()})

@permission_classes([IsAuthenticated])
class ProfileView(APIView):

    def get(self, request):
        authenticated_user: TokenUser = request.user
        if 'PATIENT' in authenticated_user.groups.values_list('name', flat=True):
            user = Patient.objects.filter(id=authenticated_user.id).first()
            serializer = PatientSerializer(user)
        else:
            user = Doctor.objects.filter(id=authenticated_user.id).first()
            serializer = DoctorSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        authenticated_user: CustomUser = request.user
        try:
            if 'PATIENT' in authenticated_user.groups.values_list('name', flat=True):
                serializer = PatientUpdateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = Patient.objects.filter(id=authenticated_user.id)
                    user.update(**serializer.validated_data)
                    if 'password' in serializer.validated_data:
                        user = Patient.objects.filter(id=authenticated_user.id).first()
                        user.set_password(serializer.validated_data['password'])
                        user.save()
                profileSerializer = PatientSerializer(data=request.data)
                profileSerializer.is_valid(raise_exception=False)
                return Response(profileSerializer.data)
            else:
                serializer = DoctorUpdateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = Doctor.objects.filter(id=authenticated_user.id)
                    user.update(**serializer.validated_data)
                    if 'password' in serializer.validated_data:
                        user = Doctor.objects.filter(id=authenticated_user.id).first()
                        user.set_password(serializer.validated_data['password'])
                        user.save()
                profileSerializer = DoctorSerializer(data=request.data)
                profileSerializer.is_valid(raise_exception=False)
                return Response(profileSerializer.data)
        except IntegrityError:
            return Response({"detail": "Invalid request. Check username, possible duplicate."}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, MedicPermission])
class PatientView(APIView):
    def post(self, request):
        try:
            serializer = AddPatientSerializer(data=request.data)
            authenticated_user: TokenUser = request.user
            current_user = Doctor.objects.get(id=authenticated_user.id)
            serializer.is_valid(raise_exception=True)
            user = Patient(**serializer.validated_data)
            user.set_password(serializer.validated_data['password'])
            group = Group.objects.get(name='PATIENT')
            user.save()
            user.groups.add(group)
            user.save()
            UserRelationship.objects.create(doctor=current_user, patient=user)
        except IntegrityError:
            return Response({"detail": "Patient exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"detail": "Patient not valid"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated, MedicPermission])
class BookingsView(APIView):
    def get(self, request):
        user_relationships = UserRelationship.objects.filter(doctor=request.user)
        patients = [relationship.patient for relationship in user_relationships]

        bookings_data = []
        bookings_today_data = []
        today = timezone.now()
        end_time = today + timedelta(days=5, hours=23, minutes=59, seconds=59)
        for patient in patients:
            today_bookings = (Booking.objects.filter(patient=patient).filter(timestamp__gte=today,timestamp__lte=end_time))
            bookings = Booking.objects.filter(patient=patient)
            for booking in bookings:
                bookings_data.append(BookingSerializer(instance=booking).data)
            for booking in today_bookings:
                bookings_today_data.append(BookingSerializer(instance=booking).data)

        return Response({
            'today': bookings_today_data,
            'all': bookings_data
        })


@permission_classes([IsAuthenticated, PatientPermission])
class PatientStatusView(APIView):
    def get(self, request):
        relationship = UserRelationship.objects.get(patient=request.user)
        bookings_data = []
        today = timezone.now()
        next_booking = Booking.objects.filter(patient=request.user).order_by('timestamp').filter(timestamp__gte=today).first()
        bookings = Booking.objects.filter(patient=request.user)
        for booking in bookings:
            context = {'doctor': relationship.doctor}
            bookings_data.append(BookingSerializer(instance=booking, context=context).data)

        next_booking_response = None
        if next_booking:
            context = {'doctor': relationship.doctor}
            booking = BookingSerializer(instance=next_booking, context=context)
            next_booking_response = booking.data
        return Response({
            'next': next_booking_response,
            'all': bookings_data
        })


@permission_classes([IsAuthenticated])
class PatientCreateBookingView(APIView):
    def post(self, request):
        authenticated_user: CustomUser = request.user
        serializer = AddBookingSerializer(data=request.data)
        if serializer.is_valid():
            if 'PATIENT' in authenticated_user.groups.values_list('name', flat=True):
                relationship = UserRelationship.objects.get(patient=request.user)
                patient = Patient.objects.filter(id=authenticated_user.id).first()
                booking = Booking.objects.create(patient=patient, requestDescription=serializer.data['requestDescription'],
                                                 timestamp=datetime.combine(date.fromisoformat(serializer.data['date']), time.fromisoformat(serializer.data['time'])))
                booking.save()
                return Response({"success": True})

@permission_classes([IsAuthenticated])
class PatientBookingView(APIView):
    def get(self, request, pk):
        authenticated_user: CustomUser = request.user
        if 'MEDIC' in authenticated_user.groups.values_list('name', flat=True):
            next_booking = Booking.objects.get(id=pk)

            next_booking_response = None
            if next_booking:
                booking = DoctorBookingSerializer(instance=next_booking)
                next_booking_response = booking.data
            return Response(next_booking_response)
        else:
            relationship = UserRelationship.objects.get(patient=request.user)
            next_booking = Booking.objects.get(id=pk)

            next_booking_response = None
            if next_booking:
                context = {'doctor': relationship.doctor}
                booking = BookingSerializer(instance=next_booking, context=context)
                next_booking_response = booking.data
            return Response(next_booking_response)
    def put(self, request, pk):
        authenticated_user: CustomUser = request.user
        if 'MEDIC' in authenticated_user.groups.values_list('name', flat=True):
            booking = Booking.objects.get(id=pk)
            if booking:
                booking.diagnosisDescription = request.data['diagnosisDescription']
                booking.save()
            return Response()


@permission_classes([IsAuthenticated, MedicPermission])
class PredictView(APIView):
    def post(self, request, pk):
        # Get the image from the request
        image = request.FILES['image']
        booking = Booking.objects.get(id=pk)
        booking.mriUploaded = image
        booking.save()
        prediction = predict_image(booking.mriUploaded.path)
        if prediction:
            if prediction != 2:
                booking.aiPrediction = "Possible tumor"
            else:
                booking.aiPrediction = "No tumor"
            booking.save()
            return Response({"result": booking.aiPrediction})
        return Response()


def predict_image(image_path):
    # Load the PyTorch model (same as in report)
    swin_model = models.swin_t(weights=models.Swin_T_Weights.IMAGENET1K_V1)
    num_ftrs = swin_model.head.in_features
    swin_model.head = nn.Linear(num_ftrs, out_features=4)
    checkpoint = torch.load('preciseMed/model_Swin_Transformer_best.pth', map_location='cpu')
    swin_model.load_state_dict(checkpoint['model_state_dict'])
    swin_model.eval()

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5), (0.5))
    ])
    img = Image.open(image_path)

    img_tensor = transform(img).unsqueeze(0)

    # Make a prediction
    with torch.no_grad():
        output = swin_model(img_tensor)
        _, predicted = torch.max(output.data, 1)

    return predicted.item()
