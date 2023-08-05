# coding: utf-8

"""
    Cythereal Dashboard API

     The API used exclusively by the MAGIC Dashboard for populating charts, graphs, tables, etc... on the dashboard.  # API Conventions  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/alerts` endpoint should return a response object with `data.alerts`. This property SHOULD  contain a list of the returned objects. For the `/alerts` endpoint, the `data.alerts` property contains a list of MagicAlerts objects. See the `/alerts` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cythereal_dashboard.api_client import ApiClient


class TablesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list_table_binaries_for_campaign(self, campaign_id, **kwargs):  # noqa: E501
        """Gets all the binaries in a specific campaign for the user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_campaign(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: The ID of a campaign. Equal to the binary_id of a random binary in the campaign. (required)
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_table_binaries_for_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_table_binaries_for_campaign_with_http_info(campaign_id, **kwargs)  # noqa: E501
            return data

    def list_table_binaries_for_campaign_with_http_info(self, campaign_id, **kwargs):  # noqa: E501
        """Gets all the binaries in a specific campaign for the user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_campaign_with_http_info(campaign_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str campaign_id: The ID of a campaign. Equal to the binary_id of a random binary in the campaign. (required)
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['campaign_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_table_binaries_for_campaign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'campaign_id' is set
        if ('campaign_id' not in params or
                params['campaign_id'] is None):
            raise ValueError("Missing the required parameter `campaign_id` when calling `list_table_binaries_for_campaign`")  # noqa: E501

        if 'campaign_id' in params and not re.search(r'^([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}|[a-fA-F0-9]{128})$', params['campaign_id']):  # noqa: E501
            raise ValueError("Invalid value for parameter `campaign_id` when calling `list_table_binaries_for_campaign`, must conform to the pattern `/^([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64}|[a-fA-F0-9]{128})$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'campaign_id' in params:
            path_params['campaign_id'] = params['campaign_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_query_param']  # noqa: E501

        return self.api_client.call_api(
            '/tables/{campaign_id}/campaign/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BinaryTableListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_table_binaries_for_campaigns(self, **kwargs):  # noqa: E501
        """Gets all the user's campaigns in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_campaigns(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_table_binaries_for_campaigns_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_table_binaries_for_campaigns_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_table_binaries_for_campaigns_with_http_info(self, **kwargs):  # noqa: E501
        """Gets all the user's campaigns in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_campaigns_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_table_binaries_for_campaigns" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_query_param']  # noqa: E501

        return self.api_client.call_api(
            '/tables/campaigns/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BinaryTableListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_table_binaries_for_investigation(self, investigation_name, **kwargs):  # noqa: E501
        """Gets all the binaries in an investigation in timeline format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_investigation(investigation_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str investigation_name: Unique user created name of a collection of files (required)
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_table_binaries_for_investigation_with_http_info(investigation_name, **kwargs)  # noqa: E501
        else:
            (data) = self.list_table_binaries_for_investigation_with_http_info(investigation_name, **kwargs)  # noqa: E501
            return data

    def list_table_binaries_for_investigation_with_http_info(self, investigation_name, **kwargs):  # noqa: E501
        """Gets all the binaries in an investigation in timeline format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_investigation_with_http_info(investigation_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str investigation_name: Unique user created name of a collection of files (required)
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['investigation_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_table_binaries_for_investigation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'investigation_name' is set
        if ('investigation_name' not in params or
                params['investigation_name'] is None):
            raise ValueError("Missing the required parameter `investigation_name` when calling `list_table_binaries_for_investigation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'investigation_name' in params:
            path_params['investigation_name'] = params['investigation_name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_query_param']  # noqa: E501

        return self.api_client.call_api(
            '/tables/{investigation_name}/investigation/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BinaryTableListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_table_binaries_for_investigations(self, **kwargs):  # noqa: E501
        """Gets all the user's investigations in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_investigations(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_table_binaries_for_investigations_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_table_binaries_for_investigations_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_table_binaries_for_investigations_with_http_info(self, **kwargs):  # noqa: E501
        """Gets all the user's investigations in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_investigations_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_table_binaries_for_investigations" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_query_param']  # noqa: E501

        return self.api_client.call_api(
            '/tables/investigations/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BinaryTableListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_table_binaries_for_singletons(self, **kwargs):  # noqa: E501
        """Gets all the user's campaigns in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_singletons(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_table_binaries_for_singletons_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_table_binaries_for_singletons_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_table_binaries_for_singletons_with_http_info(self, **kwargs):  # noqa: E501
        """Gets all the user's campaigns in table format  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_table_binaries_for_singletons_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: BinaryTableListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_table_binaries_for_singletons" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_query_param']  # noqa: E501

        return self.api_client.call_api(
            '/tables/singletons/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BinaryTableListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
