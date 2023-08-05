# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class UserSearchRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UserSearchRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'sort_order': 'str',
            'sort_by': 'str',
            'page_size': 'int',
            'page_number': 'int',
            'sort': 'list[SearchSort]',
            'expand': 'list[str]',
            'query': 'list[UserSearchCriteria]',
            'integration_presence_source': 'str',
            'enforce_permissions': 'bool'
        }

        self.attribute_map = {
            'sort_order': 'sortOrder',
            'sort_by': 'sortBy',
            'page_size': 'pageSize',
            'page_number': 'pageNumber',
            'sort': 'sort',
            'expand': 'expand',
            'query': 'query',
            'integration_presence_source': 'integrationPresenceSource',
            'enforce_permissions': 'enforcePermissions'
        }

        self._sort_order = None
        self._sort_by = None
        self._page_size = None
        self._page_number = None
        self._sort = None
        self._expand = None
        self._query = None
        self._integration_presence_source = None
        self._enforce_permissions = None

    @property
    def sort_order(self):
        """
        Gets the sort_order of this UserSearchRequest.
        The sort order for results

        :return: The sort_order of this UserSearchRequest.
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """
        Sets the sort_order of this UserSearchRequest.
        The sort order for results

        :param sort_order: The sort_order of this UserSearchRequest.
        :type: str
        """
        allowed_values = ["ASC", "DESC", "SCORE"]
        if sort_order.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for sort_order -> " + sort_order
            self._sort_order = "outdated_sdk_version"
        else:
            self._sort_order = sort_order

    @property
    def sort_by(self):
        """
        Gets the sort_by of this UserSearchRequest.
        The field in the resource that you want to sort the results by

        :return: The sort_by of this UserSearchRequest.
        :rtype: str
        """
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """
        Sets the sort_by of this UserSearchRequest.
        The field in the resource that you want to sort the results by

        :param sort_by: The sort_by of this UserSearchRequest.
        :type: str
        """
        
        self._sort_by = sort_by

    @property
    def page_size(self):
        """
        Gets the page_size of this UserSearchRequest.
        The number of results per page

        :return: The page_size of this UserSearchRequest.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this UserSearchRequest.
        The number of results per page

        :param page_size: The page_size of this UserSearchRequest.
        :type: int
        """
        
        self._page_size = page_size

    @property
    def page_number(self):
        """
        Gets the page_number of this UserSearchRequest.
        The page of resources you want to retrieve

        :return: The page_number of this UserSearchRequest.
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """
        Sets the page_number of this UserSearchRequest.
        The page of resources you want to retrieve

        :param page_number: The page_number of this UserSearchRequest.
        :type: int
        """
        
        self._page_number = page_number

    @property
    def sort(self):
        """
        Gets the sort of this UserSearchRequest.
        Multi-value sort order, list of multiple sort values

        :return: The sort of this UserSearchRequest.
        :rtype: list[SearchSort]
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """
        Sets the sort of this UserSearchRequest.
        Multi-value sort order, list of multiple sort values

        :param sort: The sort of this UserSearchRequest.
        :type: list[SearchSort]
        """
        
        self._sort = sort

    @property
    def expand(self):
        """
        Gets the expand of this UserSearchRequest.
        Provides more details about a specified resource

        :return: The expand of this UserSearchRequest.
        :rtype: list[str]
        """
        return self._expand

    @expand.setter
    def expand(self, expand):
        """
        Sets the expand of this UserSearchRequest.
        Provides more details about a specified resource

        :param expand: The expand of this UserSearchRequest.
        :type: list[str]
        """
        
        self._expand = expand

    @property
    def query(self):
        """
        Gets the query of this UserSearchRequest.


        :return: The query of this UserSearchRequest.
        :rtype: list[UserSearchCriteria]
        """
        return self._query

    @query.setter
    def query(self, query):
        """
        Sets the query of this UserSearchRequest.


        :param query: The query of this UserSearchRequest.
        :type: list[UserSearchCriteria]
        """
        
        self._query = query

    @property
    def integration_presence_source(self):
        """
        Gets the integration_presence_source of this UserSearchRequest.
        Gets an integration presence for users instead of their defaults. This parameter will only be used when presence is provided as an \"expand\". When using this parameter the maximum number of users that can be returned is 10.

        :return: The integration_presence_source of this UserSearchRequest.
        :rtype: str
        """
        return self._integration_presence_source

    @integration_presence_source.setter
    def integration_presence_source(self, integration_presence_source):
        """
        Sets the integration_presence_source of this UserSearchRequest.
        Gets an integration presence for users instead of their defaults. This parameter will only be used when presence is provided as an \"expand\". When using this parameter the maximum number of users that can be returned is 10.

        :param integration_presence_source: The integration_presence_source of this UserSearchRequest.
        :type: str
        """
        allowed_values = ["MicrosoftTeams", "ZoomPhone"]
        if integration_presence_source.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for integration_presence_source -> " + integration_presence_source
            self._integration_presence_source = "outdated_sdk_version"
        else:
            self._integration_presence_source = integration_presence_source

    @property
    def enforce_permissions(self):
        """
        Gets the enforce_permissions of this UserSearchRequest.
        Enforce view permission on request

        :return: The enforce_permissions of this UserSearchRequest.
        :rtype: bool
        """
        return self._enforce_permissions

    @enforce_permissions.setter
    def enforce_permissions(self, enforce_permissions):
        """
        Sets the enforce_permissions of this UserSearchRequest.
        Enforce view permission on request

        :param enforce_permissions: The enforce_permissions of this UserSearchRequest.
        :type: bool
        """
        
        self._enforce_permissions = enforce_permissions

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

