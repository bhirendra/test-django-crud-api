from rest_framework import serializers


class UserSignupRequestBody(serializers.Serializer):
    """
    Request body of signup API
    """
    username = serializers.CharField(help_text='Length must be 1-8 chars.', required=True)
    password = serializers.CharField(
        help_text='must contain at least one character, one number and any one of these (underscore, hyphen, hash)',
        required=True)
    email = serializers.CharField(help_text='Optional field (Input a valid email)', required=False, allow_null=True)
    mobile = serializers.IntegerField(help_text='Optional field (Input a valid 10 digits indian mobile number)', required=False, allow_null=True)


class UserLoginRequestBody(serializers.Serializer):
    """
    Request body of login API
    """
    username = serializers.CharField(help_text='Account username', required=True)
    password = serializers.CharField(help_text='Account password', required=True)


class UserProfileResponseBody(serializers.Serializer):
    """
    Response body of profile API
    """
    username = serializers.CharField(help_text='Username', required=True)
    email = serializers.CharField(help_text='Email', allow_null=True)
    mobile = serializers.CharField(help_text='Mobile number', allow_null=True)
    created = serializers.CharField(help_text='Account created time format: 30 Jun 1995, 01:00 PM')
