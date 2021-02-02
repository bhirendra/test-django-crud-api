import re
from calendar import timegm
from datetime import datetime
from functools import wraps
import jwt
import pytz
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from helper import keys, messages
from main.models import UserData
from testDjangoCrudAPI.settings import TIME_ZONE


class HelperCommon:
    """
    Common helper methods to be user across the project
    """

    @staticmethod
    def print_method_title(title):
        """
        Used to print the title of a method in proper format
        :param title:
        :return:
        """
        print("\n*********************** %s ***********************\n" % title)

    @staticmethod
    def common_response_header(request):
        """
        Method to define the common API response header data
        :param request:
        :return:
        """
        return {
            keys.TOKEN: request.META.get(keys.HTTP_TOKEN) if request.META.get(keys.HTTP_TOKEN) is not None else ''
        }

    @staticmethod
    def convert_utc_to_local_timezone(datetime_instance):
        """
        Used to convert UTC timezone to local timezone defined in settings
        :param datetime_instance:
        :return:
        """
        return datetime_instance.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE))


class HelperResponse:
    """
    All the response related common methods will come here
    """

    @staticmethod
    def response_400(request, message):
        """
        Common 400 (Bad request) response to be append
         to the API response
        :param request:
        :param message:
        :return:
        """
        return Response({
            keys.SUCCESS: keys.SUCCESS_FALSE,
            keys.ERROR_MESSAGE: message
        }, status=status.HTTP_400_BAD_REQUEST, headers=HelperCommon.common_response_header(request))


class HelperAPIValidation:
    @staticmethod
    def is_valid_username(username):
        """
        Username validation
        Conditions:
            1. Must not be blank or null.
            2. Length must be 1-8 chars.
        :param username: Given username
        :return: Boolean
        """
        if username is not None and 1 < len(username.strip()) <= 8:
            return True
        return False

    @staticmethod
    def is_valid_password(password):
        """
        Password validation
        Conditions:
            1. Must not be blank or null.
            2. Length must be 1-6 chars.
            3. Should contain at least one char.
            3. Should contain at least one digit.
            3. Should contain any one of these (underscore, hyphen, hash).
        :param password: Given password
        :return:
        """
        password_pattern = re.compile('^(?=.*[\d])(?=.*[a-zA-Z])(?=.*[_#-])[\w\d_#-]{3,6}$')
        if password is not None and password_pattern.search(password) is not None:
            return True
        return False

    @staticmethod
    def is_valid_email(email):
        """
        Email validation
        Conditions:
            1. Must be a valid email if its not blank
        :param email: Given email
        :return:
        """
        email_pattern = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
        if email is not None and email_pattern.search(email) is not None:
            return True
        return False

    @staticmethod
    def is_valid_mobile(mobile):
        """
        Mobile validation
        Conditions:
            1. Must be a valid mobile number of 10 digits
        :param mobile: Given mobile
        :return:
        """
        mobile_pattern = re.compile('^[6-9]\d{9}$')
        if mobile is not None and mobile_pattern.search(mobile) is not None:
            return True
        return False


class HelperAuthentication:

    @staticmethod
    def generate_new_token(user):
        """
        Custom method to generate token
        :param user: instance of user
        :return:
        """
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        # print("Generating Token")
        payload = jwt_payload_handler(user)
        # print("payload", payload)
        token = jwt_encode_handler(payload)
        return token, payload

    @staticmethod
    def obtain_token(request, username, password=''):
        """
        Method used to obtain a new token
        :param request: instance of request
        :param username: username
        :param password: password
        :return:
        """
        user = User.objects.get(username=username)
        if user is not None:
            token, _ = HelperAuthentication.generate_new_token(user)
            if token is not None and token != "":
                return token
            else:
                return ""
        else:
            return ""

    @staticmethod
    def verify_token(request, obtained_token):
        """
        Method used to verify the token
        :return:
        """
        import jwt
        from rest_framework_jwt.authentication import jwt_decode_handler, jwt_get_username_from_payload
        from django.contrib.auth.models import User
        try:
            """ Decode token """
            payload = jwt_decode_handler(obtained_token)

            """Verify token """
            username = jwt_get_username_from_payload(payload)
            if not username:
                # Invalid payload
                return False, None, None
            # Make sure user exists
            try:
                user = User.objects.get_by_natural_key(username)
            except User.DoesNotExist:
                # User doesn't exist.
                return False, None, None
            if not user.is_active:
                # User account is disabled
                return False, None, None
            return True, payload, user
        except jwt.ExpiredSignature:
            # Signature has expired
            return False, None, None
        except jwt.DecodeError:
            return False, None, None

    @staticmethod
    def decode_access_token(encoded):
        """
        Returns decoded user id from access token
        :param encoded: encoded token
        :return:
        """
        try:
            decoded_json = jwt.decode(encoded, verify=False)
            return decoded_json
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignature, jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidKeyError, jwt.exceptions.InvalidTokenError):
            return None

    @staticmethod
    def authenticate_user_access_token(request):
        """
        Custom method used to verify access token
        :param request:
        :return:
        """
        msg = messages.AUTHENTICATION_REQUIRED
        if keys.HTTP_TOKEN in request.META:
            token = request.META.get(keys.HTTP_TOKEN)
            """ verify token """
            decoded_json = HelperAuthentication.decode_access_token(token)
            # If decoded Json is None, then send login time out
            if decoded_json is None or not decoded_json:
                return {
                    keys.STATUS_CODE: keys.HTTP_440_LOGIN_TIME_OUT,
                    keys.ERROR_MESSAGE: messages.INVALID_TOKEN
                }
            try:
                _ = UserData.objects.get(user__username=decoded_json[keys.USERNAME])
            except UserData.DoesNotExist:
                pass
            if decoded_json is not None:
                is_token_not_expired = HelperAuthentication.verify_token(request, token)
                if is_token_not_expired:
                    return {
                        keys.STATUS_CODE: status.HTTP_200_OK,
                        keys.USERNAME: decoded_json.get(keys.USERNAME)
                    }
                else:
                    return {
                        keys.STATUS_CODE: keys.HTTP_440_LOGIN_TIME_OUT,
                        keys.ERROR_MESSAGE: messages.SESSION_EXPIRED
                    }
            else:
                return {
                    keys.STATUS_CODE: keys.HTTP_440_LOGIN_TIME_OUT,
                    keys.ERROR_MESSAGE: messages.SESSION_EXPIRED
                }
        return {
            keys.STATUS_CODE: status.HTTP_403_FORBIDDEN,
            keys.ERROR_MESSAGE: msg,
            keys.USERNAME: None
        }

    @staticmethod
    def validate_access_token(function):
        """
        Custom decorator to verify user access token
        :param function:
        :return:
        """
        @wraps(function)
        def wrap(request, *args, **kwargs):
            res = HelperAuthentication.authenticate_user_access_token(request)
            # print("res ", res)
            if res.get(keys.STATUS_CODE) != status.HTTP_200_OK:
                return Response(data={keys.ERROR_MESSAGE: res.get(keys.ERROR_MESSAGE)},
                                status=res.get(keys.STATUS_CODE))
            return function(request, *args, **kwargs)
        return wrap


def jwt_custom_payload_handler(django_user):
    """
    Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    :param django_user: instance of user
    :return:
    """
    from rest_framework_jwt.settings import api_settings
    return {
        keys.USERNAME: django_user.username,
        keys.EXP: datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        keys.ORIG_IAT: timegm(
            datetime.utcnow().utctimetuple()
        )
    }
