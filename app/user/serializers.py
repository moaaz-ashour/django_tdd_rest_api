from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

        # the password should be write only.
        # it should not be serialized when get is called
        # we specify extra kwargs for each field
        # list of accepted args for can be found under core argument section of
        # https://www.django-rest-framework.org/api-guide/fields/
        # for password field, args under serializer.CharField are also valid
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    # create() is called when we use the CreateAPI view
    # which takes a POST request to create a user
    def create(self, validated_data):
        """Create a new user with encrypted password and return it
        """
        return get_user_model().objects.create_user(**validated_data)