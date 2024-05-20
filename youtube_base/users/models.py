from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    The Profile model represents the user profile in the system. Each user has one profile, which
    stores additional information about the user that is not stored in the User model.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    subscriptions = models.ManyToManyField('youtubers.Youtuber', related_name='profiles',
                                           blank=True)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f'Профіль користувача {self.user.username}'
