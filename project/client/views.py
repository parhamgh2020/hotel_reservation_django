from .serializers import UserSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.contrib.auth.models import User


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    ViewSet for creating, retrieving and listing users.

    list:
    Returns a paginated list of all users.

    retrieve:
    Returns the details of a single user.

    create:
    Creates a new user with the given parameters.

    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
