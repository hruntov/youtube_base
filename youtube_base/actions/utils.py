import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from youtube_base.actions.models import Action


def create_action(user, action, target=None):
    """
    Create an action if no similar action was created in the last minute.

    Args:
        user (User): The User instance performing the action.
        action (str): A string describing the action performed.
        target (Optional[Model]): The Django model instance that the action is targeting.

    Returns:
        (bool): A boolean value. True if a new action was created, False otherwise.

    """
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user=user.id,
                                            action=action,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        action = Action(user=user, action=action, target=target)
        action.save()
        return True
    return False
