"""
Handlers to process the responses from the Humble Bundle API
"""

__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

from humblebundle.exceptions import *
from humblebundle.models import *

import itertools
import requests


# Helper methods


def parse_data(response):
    try:
        return response.json()
    except ValueError as e:
        raise HumbleParseException("Invalid JSON: %s", str(e), request=response.request, response=response)


def get_errors(data):
    errors = data.get('errors', None)
    error_msg = ", ".join(itertools.chain.from_iterable(v for k, v in errors.items())) \
        if errors else "Unspecified error"
    return errors, error_msg


def authenticated_response_helper(response, data):
    # Successful API calls might not have a success property.
    # It's not enough to check if it's falsy, as None is acceptable

    success = data.get('success', None)
    if success is True:
        return True

    error_id = data.get('error_id', None)
    errors, error_msg = get_errors(data)

    # API calls that require login and have a missing or invalid token
    if error_id == 'login_required':
        raise HumbleAuthenticationException(error_msg, request=response.request, response=response)

    # Something happened, we're not sure what but we hope the error_msg is useful
    if success is False or errors is not None or error_id is not None:
        raise HumbleResponseException(error_msg, request=response.request, response=response)

    # Response had no success or errors fields, it's probably data
    return True


# Response handlers


def login_handler(client, response):
    """ login response always returns JSON """

    data = parse_data(response)

    success = data.get('success', None)
    if success is True:
        return True

    captcha_required = data.get('captcha_required')
    authy_required = data.get('authy_required')

    errors, error_msg = get_errors(data)
    if errors:
        captcha = errors.get('captcha')
        if captcha:
            raise HumbleCaptchaException(error_msg, request=response.request, response=response,
                                         captcha_required=captcha_required, authy_required=authy_required)

        username = errors.get('username')
        if username:
            raise HumbleCredentialException(error_msg, request=response.request, response=response,
                                            captcha_required=captcha_required, authy_required=authy_required)

        authy_token = errors.get("authy-token")
        if authy_token:
            raise HumbleTwoFactorException(error_msg, request=response.request, response=response,
                                           captcha_required=captcha_required, authy_required=authy_required)

    raise HumbleAuthenticationException(error_msg, request=response.request, response=response,
                                        captcha_required=captcha_required, authy_required=authy_required)


def order_list_handler(client, response):
    """ order_list response always returns JSON """

    data = parse_data(response)

    if isinstance(data, list):
        return [Order(client, order) for order in data]

    # Let the helper function raise any common exceptions
    authenticated_response_helper(response, data)

    # We didn't get a list, or an error message
    raise HumbleResponseException("Unexpected response body", request=response.request, response=response)


def order_handler(client, response):
    """ order response might be 404 with no body if not found """

    if response.status_code == requests.codes.not_found:
        raise HumbleResponseException("Order not found", request=response.request, response=response)

    data = parse_data(response)

    # The helper function should be sufficient to catch any other errors
    if authenticated_response_helper(response, data):
        return Order(client, data)


def claimed_entities_handler(client, response):
    """
    claimed_entities response always returns JSON
    returns parsed json dict
    """

    data = parse_data(response)

    # The helper function should be sufficient to catch any errors
    if authenticated_response_helper(response, data):
        return data


def sign_download_url_handler(client, response):
    """ sign_download_url response always returns JSON """

    data = parse_data(response)

    # If the request is unauthorized (this includes invalid machine names) this response has it's own error syntax
    errors = data.get('_errors', None)
    message = data.get('_message', None)

    if errors:
        error_msg = "%s: %s" % (errors, message)
        raise HumbleResponseException(error_msg, request=response.request, response=response)

    # If the user isn't signed in we get a "typical" error response
    if authenticated_response_helper(response, data):
        return data['signed_url']