from rest_framework.decorators import api_view


@api_view(['POST'])
def signup(request):
    return 0


@api_view(['POST'])
def login(request):
    return 0


@api_view(['GET'])
def profile(request):
    return 0


@api_view(['POST'])
def logout(request):
    """
    THIS API is not needed because existance of token can be managed from the
    frontend application.
    Deleting the token will act as logout.
    :param request:
    :return:
    """
    return 0
