import datetime
import sys
import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import PIL.Image
import os

from finalReport import settings


# Create your models here.

class Specialization(models.TextChoices):
    MEDICAL = 'MEDICAL'
    SURGICAL = 'SURGICAL'
    RADIATION = 'RADIATION'
    NEURO = 'NEURO'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    city = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Patient(CustomUser):
    dateOfBirth = models.DateField(blank=True, null=True)
    hasInsurance = models.BooleanField(default=False)
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    previousConditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

class Doctor(CustomUser):
    specialization = models.CharField(max_length=50, choices=Specialization.choices, default=Specialization.MEDICAL)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

class UserRelationship(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_relationships')
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, related_name='patient_relationships')



class Booking(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_bookings')
    timestamp = models.DateTimeField()
    requestDescription = models.TextField()
    diagnosisDescription = models.TextField(null=True, blank=True)
    aiPrediction = models.TextField(null=True, blank=True)
    mriUploaded = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.mriUploaded:
            try:
                img = PIL.Image.open(self.mriUploaded)
                img.verify()
                # reopen because img.verify() moves pointer to the end of the file
                img = PIL.Image.open(self.mriUploaded)

                # convert png to RGB
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Resize the image
                img = img.resize((500, 500), PIL.Image.LANCZOS)

                # Prepare the image for saving
                temp_img = BytesIO()
                # Save the image as JPEG
                img.save(temp_img, format="JPEG", quality=100, optimize=True)
                temp_img.seek(0)

                # Change file extension to .jpg
                img = f"{self.id}.jpg"

                path = os.path.join(settings.MEDIA_ROOT, img)
                if os.path.exists(path):
                    os.remove(path)

                # Save the BytesIO object to the ImageField with the new filename
                self.mriUploaded.save(img, ContentFile(temp_img.read()), save=False)

            except (IOError, SyntaxError) as e:
                raise ValueError(f"The uploaded file is not a valid image. -- {e}")
        else:
            path = os.path.join(settings.MEDIA_ROOT,f"{self.id}.jpg" )
            if os.path.exists(path):
                os.remove(path)

        super().save(*args, **kwargs)