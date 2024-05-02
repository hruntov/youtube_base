from django.contrib.auth.models import User

from .models import Profile


class EmailAuthBackend:
    """Сustom authentication backend that authenticates users based on their email and password."""
    def authenticate(self, request, username=None, password=None):
        """
        Authenticate a user based on email (username) and password.

        Args:
            request: The request object.
            username (str): The user's email.
            password (str): The user's password.

        Returns:
            The authenticated user, or None if authentication fails.

        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            The user with the given ID, or None if no such user exists.

        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Create a user profile when a new user is registered.

    Args:
        backend: The authentication backend.
        user: The user object.

    """
    Profile.objects.get_or_create(user=user)
