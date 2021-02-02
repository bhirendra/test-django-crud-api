from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from helper import keys


class ResponseCustomMiddleware(MiddlewareMixin):
    """
    Override DRF Response
    send status code in json

    Format of Error Response
    {
    "error": {
            "message": "Describe error message here"
        }
    }
    Format of Header
    {
    "token": "value of token"
    }
    """

    def __init__(self, *args, **kwargs):
        super(ResponseCustomMiddleware, self).__init__(*args, **kwargs)

    def process_template_response(self, request, response):
        if not response.is_rendered and isinstance(response, Response):
            if isinstance(response.data, dict):
                """ Format error message """
                if keys.ERROR_MESSAGE in response.data:
                    response.data[keys.ERROR] = {keys.MESSAGE: response.data.get(keys.ERROR_MESSAGE)}
                    del response.data[keys.ERROR_MESSAGE]

                """ Append message if its not there """
                if keys.MESSAGE not in response.data:
                    response.data[keys.MESSAGE] = keys.SUCCESS

                if keys.TOKEN not in response._headers:
                    response._headers[keys.TOKEN] = (keys.TOKEN, '')

                if response.data.get(keys.SUCCESS) == keys.SUCCESS_FALSE:
                    response.data[keys.MESSAGE] = keys.FAILURE

                """ If status code is not 200 then get the error message from 'detail' key """
                if response.status_code != 200:
                    response.data[keys.MESSAGE] = keys.FAILURE
                    if keys.DETAIL in response.data:
                        response.data[keys.ERROR] = {keys.MESSAGE: response.data.get(keys.DETAIL)}
                        del response.data[keys.DETAIL]

                # you can add you logic for checking in status code is 2** or 4**.
                response.data.setdefault(keys.STATUS_CODE, response.status_code)
        return response
