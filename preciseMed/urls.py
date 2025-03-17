from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, ProfileView, PatientView, BookingsView, PatientStatusView, PatientBookingView, \
    PredictView, HealthCheckView, PatientCreateBookingView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="healthcheck"),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/patient/', PatientView.as_view(), name='patient'),
    path('api/create-booking/', PatientCreateBookingView.as_view(), name='create-booking'),
    path('api/bookings/', BookingsView.as_view(), name='dashboard'),
    path('api/patient-status/', PatientStatusView.as_view(), name='patient-status'),
    path('api/bookings/<int:pk>/', PatientBookingView.as_view(), name='patient-booking'),
    path('api/predict/<int:pk>/', PredictView.as_view(), name='predict-booking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
