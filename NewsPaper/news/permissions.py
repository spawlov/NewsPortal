from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


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
