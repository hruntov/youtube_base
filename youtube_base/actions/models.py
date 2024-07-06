from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    """
    Represents an action performed by a user.

    Attributes:
        user (ForeignKey): A reference to the User model.
        action (CharField): Describes the action performed by the user.
        created (DateTimeField): The date and time when the action was created.
        target_ct (ForeignKey): A reference to the ContentType model, allowing the action to be
            associated with any model.
        target_id (PositiveIntegerField): The ID of the target object the action is associated with.
            Used in conjunction with 'target_ct' to point to specific instances of any model.
        target (GenericForeignKey): A generic foreign key to the target object, determined by
            'target_ct' and 'target_id'.

    """
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        app_label = 'actions'
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])
        ]
        ordering = ['-created']
