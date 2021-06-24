from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

# Wrap the texts with this if you want django to automatically translate
from django.utils.translation import ugettext_lazy as _


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


class AuthTokenSerializer(serializers.Serializer):
    """
        Serializer for user authentication object:
        - Serializer can also be used without a model
        - Since this is not a model, we inherit from serializers.Serializer
        - We will get some data from user, validate it and return some value
    """
    # create fields to get data for authentication
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ override validate method and raise exception if invalid
            it is called when we validate our serializers
            attrs: every field which makes up the serializer
        """
        # attrs contains all the serializer fields defined above
        # retrieve email and password from attrs
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # if authentication fails:
        if not user:
            # we use gettext to enable language tranlation for this text
            msg = _("Unable to authenticate with credentials provided")
            # raise the relavant http status code
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
