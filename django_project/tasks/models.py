from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import Optional, Tuple


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username


class BreedLikeManager(models.Manager):
    def filter(self, *args, **kwargs) -> models.QuerySet['BreedLike']:
        return super().filter(*args, **kwargs)

    def update_or_create(
            self,
            defaults: Optional[dict] = None,
            **kwargs
    ) -> Tuple['BreedLike', bool]:
        return super().update_or_create(defaults=defaults, **kwargs)


class BreedLike(models.Model):
    objects = BreedLikeManager()
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    breed_name = models.CharField(max_length=100)
    value = models.SmallIntegerField()  # 1 = like, -1 = dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'breed_name')