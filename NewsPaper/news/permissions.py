from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class PermissionAndOwnerRequiredMixin(PermissionRequiredMixin):
    """Дополнительная проверка на владельца поста"""
    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object() \
                .author_post.author_user.id == self.request.user.id:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class ProfileOwnerRequiredMixin(PermissionRequiredMixin):
    """Дополнительная проверка на владельца profile"""
    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().id == self.request.user.id:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.groups.filter(name='authors').exists())


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_post.author_user.id == request.user.id
