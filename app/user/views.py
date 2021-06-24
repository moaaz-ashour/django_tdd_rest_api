from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """view for API validating user credentials and providing token
    """
    serializer_class = AuthTokenSerializer
    # class that will render this page
    # works without this but does not create nice view in the browser
    # as it did when extended from generic views
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES