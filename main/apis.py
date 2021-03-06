from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from helper import keys, messages, doc_descriptions, doc_serializers
from helper.views import HelperCommon, HelperResponse, HelperAPIValidation, HelperAuthentication
from main.models import UserData
from main.serializers import UserDataSerializer


@swagger_auto_schema(
    operation_id='User Signup API', operation_description=doc_descriptions.API_USER_SIGNUP,
    method='post', responses={
        200: 'Token will be sent in header and a welcome message in body',
        400: 'Invalid credentials'
    },
    request_body=doc_serializers.UserSignupRequestBody
)
@api_view(['POST'])
def signup(request):
    """
    User Signup API
    :param request:
    :return:
    """
    HelperCommon.print_method_title("API-Signup")
    username = request.data.get(keys.USERNAME) or ''
    password = request.data.get(keys.PASSWORD) or ''
    email = request.data.get(keys.EMAIL) or ''
    mobile = request.data.get(keys.MOBILE) or ''

    """ Validate request data """
    # Username validation
    if not HelperAPIValidation.is_valid_username(username.strip()):
        return HelperResponse.response_400(request, messages.VALID_USERNAME)

    # Password Validation
    if not HelperAPIValidation.is_valid_password(password.strip()):
        return HelperResponse.response_400(request, messages.VALID_PASSWORD)

    # Email Validation if filled something
    if email is not None and email.strip() != '' and not HelperAPIValidation.is_valid_email(email.strip()):
        return HelperResponse.response_400(request, messages.INVALID_EMAIL)

    # Mobile Validation if filled something
    if mobile is not None and mobile.strip() != '' and not HelperAPIValidation.is_valid_mobile(mobile.strip()):
        return HelperResponse.response_400(request, messages.VALID_MOBILE)

    # Validate existence of username
    if UserData.objects.filter(user__username=username).exists():
        return HelperResponse.response_400(request, messages.USERNAME_ALREADY_EXISTS)
    else:
        django_user = User.objects.create_user(username=username, email=email)
        django_user.set_password(password)
        django_user.save()
        UserData.objects.create(
            user=django_user,
            email=email,
            mobile=int(mobile) if str(mobile).isdigit() else None
        )
        response = {
            keys.MESSAGE: messages.WELCOME_USERNAME.format(username=username)
        }
        token = HelperAuthentication.obtain_token(request, username=username, password=password)
        return Response(response, status=status.HTTP_200_OK, headers={keys.TOKEN: token})


@swagger_auto_schema(
    operation_id='User Login API', operation_description=doc_descriptions.API_USER_LOGIN,
    method='post', responses={
        200: 'Token will be sent in header and a welcome message in body',
        400: 'Invalid credentials',
    },
    request_body=doc_serializers.UserLoginRequestBody
)
@api_view(['POST'])
def login(request):
    """
    User Login API
    :param request:
    :return:
    """
    HelperCommon.print_method_title("API-Login")
    username = request.data.get(keys.USERNAME) or None
    password = request.data.get(keys.PASSWORD) or None
    django_user = authenticate(request, username=username, password=password)
    if django_user is not None:
        # User exists
        response = {
            keys.MESSAGE: messages.WELCOME_USERNAME.format(username=username)
        }
        token = HelperAuthentication.obtain_token(request, username=username, password=password)
        return Response(response, status=status.HTTP_200_OK, headers={keys.TOKEN: token})
    else:
        # Invalid credentials
        return HelperResponse.response_400(request, messages.INVALID_CREDENTIALS)


@swagger_auto_schema(
    operation_id='User Profile API', operation_description=doc_descriptions.API_USER_LOGIN,
    manual_parameters=[openapi.Parameter(keys.TOKEN, openapi.IN_HEADER, type=openapi.TYPE_STRING, required=True)],
    method='get', response={
        200: doc_serializers.UserProfileResponseBody
    }
)
@api_view(['GET'])
@HelperAuthentication.validate_access_token
def profile(request):
    """
    User Profile GET API
    :param request:
    :return:
    """
    HelperCommon.print_method_title("API- User Profile")
    try:
        decoded_json = HelperAuthentication.decode_access_token(HelperCommon.get_meta_token(request.META))
        username = decoded_json[keys.USERNAME]
        # Get the instance of the user
        user_instance = UserData.objects.get(user__username=username)
        # Get profile data from serializer
        serializer = UserDataSerializer(user_instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=HelperCommon.common_response_header(request))
    except Exception as e:
        return HelperResponse.response_400(request, str(e))


@api_view(['POST'])
def logout(request):
    """
    "JWT is stateless"
    THIS API is not needed because existence of token can be managed from the
    frontend application.
    Deleting the token will act as logout.
    :param request:
    :return:
    """
    return 0
