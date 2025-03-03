from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import *

# Register your models here.
class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient')


class PatientAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Patient
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'dateOfBirth', 'city', 'telephone', 'hasInsurance', 'allergies', 'previousConditions', 'medications', 'groups',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'dateOfBirth', 'city', 'telephone', 'hasInsurance', 'allergies', 'previousConditions', 'medications', 'groups', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)

class DoctorAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Patient
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'city', 'telephone', 'specialization', 'groups',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'city', 'telephone', 'specialization', 'groups', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)

class BookingsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'timestamp', 'requestDescription', 'diagnosisDescription')


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Booking, BookingsAdmin)
admin.site.register(UserRelationship, UserRelationshipAdmin)