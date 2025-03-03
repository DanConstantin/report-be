from rest_framework.permissions import BasePermission

class MedicPermission(BasePermission):
    def has_permission(self, request, view):
        role = request.auth['role']

        return role == 'MEDIC'

class PatientPermission(BasePermission):
    def has_permission(self, request, view):
        role = request.auth['role']

        return role == 'PATIENT'

class GuestPermission(BasePermission):
    def has_permission(self, request, view):
        return True