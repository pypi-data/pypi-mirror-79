# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.09.08
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from agilicus_api.api_client import ApiClient
from agilicus_api.exceptions import (
    ApiTypeError,
    ApiValueError
)


class TokensApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_introspect_token(self, token_introspect, **kwargs):  # noqa: E501
        """Introspect a token  # noqa: E501

        Introspect a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_introspect_token(token_introspect, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenIntrospect token_introspect: Token to introspect (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Token
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_introspect_token_with_http_info(token_introspect, **kwargs)  # noqa: E501

    def create_introspect_token_with_http_info(self, token_introspect, **kwargs):  # noqa: E501
        """Introspect a token  # noqa: E501

        Introspect a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_introspect_token_with_http_info(token_introspect, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenIntrospect token_introspect: Token to introspect (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Token, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['token_introspect']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_introspect_token" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'token_introspect' is set
        if self.api_client.client_side_validation and ('token_introspect' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_introspect'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_introspect` when calling `create_introspect_token`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'token_introspect' in local_var_params:
            body_params = local_var_params['token_introspect']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens/introspect', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Token',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_reissued_token(self, token_reissue_request, **kwargs):  # noqa: E501
        """Issue a new token from another  # noqa: E501

        Issues a new token with the same or reduced scope to the one presented. Use this to retrieve a token for accessing a different organisation than the one you're currently operating on. Note that the presented token remains valid if it already was. If it is not valid, or the you do not have permissions in the requested organisation, the request will fail. The token will expire at the same time as the presented token.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_reissued_token(token_reissue_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenReissueRequest token_reissue_request: The token request (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: RawToken
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_reissued_token_with_http_info(token_reissue_request, **kwargs)  # noqa: E501

    def create_reissued_token_with_http_info(self, token_reissue_request, **kwargs):  # noqa: E501
        """Issue a new token from another  # noqa: E501

        Issues a new token with the same or reduced scope to the one presented. Use this to retrieve a token for accessing a different organisation than the one you're currently operating on. Note that the presented token remains valid if it already was. If it is not valid, or the you do not have permissions in the requested organisation, the request will fail. The token will expire at the same time as the presented token.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_reissued_token_with_http_info(token_reissue_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenReissueRequest token_reissue_request: The token request (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(RawToken, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['token_reissue_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_reissued_token" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'token_reissue_request' is set
        if self.api_client.client_side_validation and ('token_reissue_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_reissue_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_reissue_request` when calling `create_reissued_token`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'token_reissue_request' in local_var_params:
            body_params = local_var_params['token_reissue_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens/reissue', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RawToken',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_revoke_token_task(self, token_revoke, **kwargs):  # noqa: E501
        """Revoke a token  # noqa: E501

        Revoke a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_revoke_token_task(token_revoke, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenRevoke token_revoke: Token to revoke (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_revoke_token_task_with_http_info(token_revoke, **kwargs)  # noqa: E501

    def create_revoke_token_task_with_http_info(self, token_revoke, **kwargs):  # noqa: E501
        """Revoke a token  # noqa: E501

        Revoke a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_revoke_token_task_with_http_info(token_revoke, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param TokenRevoke token_revoke: Token to revoke (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['token_revoke']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_revoke_token_task" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'token_revoke' is set
        if self.api_client.client_side_validation and ('token_revoke' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_revoke'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_revoke` when calling `create_revoke_token_task`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'token_revoke' in local_var_params:
            body_params = local_var_params['token_revoke']
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens/revoke', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_token(self, create_token_request, **kwargs):  # noqa: E501
        """Create a token  # noqa: E501

        Create a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_token(create_token_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateTokenRequest create_token_request: Rule to sign (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: RawToken
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_token_with_http_info(create_token_request, **kwargs)  # noqa: E501

    def create_token_with_http_info(self, create_token_request, **kwargs):  # noqa: E501
        """Create a token  # noqa: E501

        Create a token  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_token_with_http_info(create_token_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateTokenRequest create_token_request: Rule to sign (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(RawToken, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['create_token_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_token" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'create_token_request' is set
        if self.api_client.client_side_validation and ('create_token_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['create_token_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `create_token_request` when calling `create_token`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_token_request' in local_var_params:
            body_params = local_var_params['create_token_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RawToken',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_token_validation(self, create_token_request, **kwargs):  # noqa: E501
        """Validate a token request  # noqa: E501

        Validate a token request prior to creating a token. This verifies the user has permission to access the scopes requested  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_token_validation(create_token_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateTokenRequest create_token_request: Token to validate (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CreateTokenRequest
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_token_validation_with_http_info(create_token_request, **kwargs)  # noqa: E501

    def create_token_validation_with_http_info(self, create_token_request, **kwargs):  # noqa: E501
        """Validate a token request  # noqa: E501

        Validate a token request prior to creating a token. This verifies the user has permission to access the scopes requested  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_token_validation_with_http_info(create_token_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CreateTokenRequest create_token_request: Token to validate (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CreateTokenRequest, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['create_token_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_token_validation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'create_token_request' is set
        if self.api_client.client_side_validation and ('create_token_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['create_token_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `create_token_request` when calling `create_token_validation`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_token_request' in local_var_params:
            body_params = local_var_params['create_token_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens/validations', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateTokenRequest',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_tokens(self, **kwargs):  # noqa: E501
        """Query tokens  # noqa: E501

        Query tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tokens(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit the number of rows in the response
        :param str sub: search criteria sub
        :param str exp_from: search criteria expired from using dateparser
        :param str exp_to: search criteria expired to using dateparser
        :param str iat_from: search criteria issued from using dateparser
        :param str iat_to: search criteria issued to using dateparser
        :param str jti: search criteria using jti
        :param str org: search criteria using org
        :param bool revoked: search criteria for revoked tokens
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ListTokensResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_tokens_with_http_info(**kwargs)  # noqa: E501

    def list_tokens_with_http_info(self, **kwargs):  # noqa: E501
        """Query tokens  # noqa: E501

        Query tokens  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tokens_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit the number of rows in the response
        :param str sub: search criteria sub
        :param str exp_from: search criteria expired from using dateparser
        :param str exp_to: search criteria expired to using dateparser
        :param str iat_from: search criteria issued from using dateparser
        :param str iat_to: search criteria issued to using dateparser
        :param str jti: search criteria using jti
        :param str org: search criteria using org
        :param bool revoked: search criteria for revoked tokens
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ListTokensResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['limit', 'sub', 'exp_from', 'exp_to', 'iat_from', 'iat_to', 'jti', 'org', 'revoked']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_tokens" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 100:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_tokens`, must be a value less than or equal to `100`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_tokens`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'sub' in local_var_params and local_var_params['sub'] is not None:  # noqa: E501
            query_params.append(('sub', local_var_params['sub']))  # noqa: E501
        if 'exp_from' in local_var_params and local_var_params['exp_from'] is not None:  # noqa: E501
            query_params.append(('exp_from', local_var_params['exp_from']))  # noqa: E501
        if 'exp_to' in local_var_params and local_var_params['exp_to'] is not None:  # noqa: E501
            query_params.append(('exp_to', local_var_params['exp_to']))  # noqa: E501
        if 'iat_from' in local_var_params and local_var_params['iat_from'] is not None:  # noqa: E501
            query_params.append(('iat_from', local_var_params['iat_from']))  # noqa: E501
        if 'iat_to' in local_var_params and local_var_params['iat_to'] is not None:  # noqa: E501
            query_params.append(('iat_to', local_var_params['iat_to']))  # noqa: E501
        if 'jti' in local_var_params and local_var_params['jti'] is not None:  # noqa: E501
            query_params.append(('jti', local_var_params['jti']))  # noqa: E501
        if 'org' in local_var_params and local_var_params['org'] is not None:  # noqa: E501
            query_params.append(('org', local_var_params['org']))  # noqa: E501
        if 'revoked' in local_var_params and local_var_params['revoked'] is not None:  # noqa: E501
            query_params.append(('revoked', local_var_params['revoked']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['token-valid']  # noqa: E501

        return self.api_client.call_api(
            '/v1/tokens', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListTokensResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
