from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('HUIIIIIIIIIIIIIIIIIIi')
        if request.user.is_staff:
            print('staff')
            return True
        print('obj.buyer', obj.buyer, 'request.user', request.user, obj.buyer == request.user)
        return obj.buyer == request.user


class IsOwnerReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
