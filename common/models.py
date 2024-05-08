from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        db_table = 'custom_user'

    # related_name을 추가해 충돌을 해결합니다.
    groups = models.ManyToManyField(
        verbose_name=_('groups'),
        to='auth.Group',
        blank=True,
        help_text=_('Specific groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        verbose_name=_('user permissions'),
        to='auth.Permission',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
