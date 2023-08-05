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

class ScimServiceProviderConfig(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ScimServiceProviderConfig - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'schemas': 'list[str]',
            'documentation_uri': 'str',
            'patch': 'ScimServiceProviderConfigSimpleFeature',
            'filter': 'ScimServiceProviderConfigFilterFeature',
            'etag': 'ScimServiceProviderConfigSimpleFeature',
            'sort': 'ScimServiceProviderConfigSimpleFeature',
            'bulk': 'ScimServiceProviderConfigBulkFeature',
            'change_password': 'ScimServiceProviderConfigSimpleFeature',
            'authentication_schemes': 'list[ScimServiceProviderConfigAuthenticationScheme]',
            'meta': 'ScimMetadata'
        }

        self.attribute_map = {
            'schemas': 'schemas',
            'documentation_uri': 'documentationUri',
            'patch': 'patch',
            'filter': 'filter',
            'etag': 'etag',
            'sort': 'sort',
            'bulk': 'bulk',
            'change_password': 'changePassword',
            'authentication_schemes': 'authenticationSchemes',
            'meta': 'meta'
        }

        self._schemas = None
        self._documentation_uri = None
        self._patch = None
        self._filter = None
        self._etag = None
        self._sort = None
        self._bulk = None
        self._change_password = None
        self._authentication_schemes = None
        self._meta = None

    @property
    def schemas(self):
        """
        Gets the schemas of this ScimServiceProviderConfig.
        The list of supported schemas.

        :return: The schemas of this ScimServiceProviderConfig.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this ScimServiceProviderConfig.
        The list of supported schemas.

        :param schemas: The schemas of this ScimServiceProviderConfig.
        :type: list[str]
        """
        
        self._schemas = schemas

    @property
    def documentation_uri(self):
        """
        Gets the documentation_uri of this ScimServiceProviderConfig.
        The HTTP-addressable URL that points to the service provider's documentation.

        :return: The documentation_uri of this ScimServiceProviderConfig.
        :rtype: str
        """
        return self._documentation_uri

    @documentation_uri.setter
    def documentation_uri(self, documentation_uri):
        """
        Sets the documentation_uri of this ScimServiceProviderConfig.
        The HTTP-addressable URL that points to the service provider's documentation.

        :param documentation_uri: The documentation_uri of this ScimServiceProviderConfig.
        :type: str
        """
        
        self._documentation_uri = documentation_uri

    @property
    def patch(self):
        """
        Gets the patch of this ScimServiceProviderConfig.
        The \"patch\" configuration options.

        :return: The patch of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigSimpleFeature
        """
        return self._patch

    @patch.setter
    def patch(self, patch):
        """
        Sets the patch of this ScimServiceProviderConfig.
        The \"patch\" configuration options.

        :param patch: The patch of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigSimpleFeature
        """
        
        self._patch = patch

    @property
    def filter(self):
        """
        Gets the filter of this ScimServiceProviderConfig.
        The \"filter\" configuration options.

        :return: The filter of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigFilterFeature
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """
        Sets the filter of this ScimServiceProviderConfig.
        The \"filter\" configuration options.

        :param filter: The filter of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigFilterFeature
        """
        
        self._filter = filter

    @property
    def etag(self):
        """
        Gets the etag of this ScimServiceProviderConfig.
        The \"etag\" configuration options.

        :return: The etag of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigSimpleFeature
        """
        return self._etag

    @etag.setter
    def etag(self, etag):
        """
        Sets the etag of this ScimServiceProviderConfig.
        The \"etag\" configuration options.

        :param etag: The etag of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigSimpleFeature
        """
        
        self._etag = etag

    @property
    def sort(self):
        """
        Gets the sort of this ScimServiceProviderConfig.
        The \"sort\" configuration options.

        :return: The sort of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigSimpleFeature
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """
        Sets the sort of this ScimServiceProviderConfig.
        The \"sort\" configuration options.

        :param sort: The sort of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigSimpleFeature
        """
        
        self._sort = sort

    @property
    def bulk(self):
        """
        Gets the bulk of this ScimServiceProviderConfig.
        The \"bulk\" configuration options.

        :return: The bulk of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigBulkFeature
        """
        return self._bulk

    @bulk.setter
    def bulk(self, bulk):
        """
        Sets the bulk of this ScimServiceProviderConfig.
        The \"bulk\" configuration options.

        :param bulk: The bulk of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigBulkFeature
        """
        
        self._bulk = bulk

    @property
    def change_password(self):
        """
        Gets the change_password of this ScimServiceProviderConfig.
        The \"changePassword\" configuration options.

        :return: The change_password of this ScimServiceProviderConfig.
        :rtype: ScimServiceProviderConfigSimpleFeature
        """
        return self._change_password

    @change_password.setter
    def change_password(self, change_password):
        """
        Sets the change_password of this ScimServiceProviderConfig.
        The \"changePassword\" configuration options.

        :param change_password: The change_password of this ScimServiceProviderConfig.
        :type: ScimServiceProviderConfigSimpleFeature
        """
        
        self._change_password = change_password

    @property
    def authentication_schemes(self):
        """
        Gets the authentication_schemes of this ScimServiceProviderConfig.
        The list of supported authentication schemes.

        :return: The authentication_schemes of this ScimServiceProviderConfig.
        :rtype: list[ScimServiceProviderConfigAuthenticationScheme]
        """
        return self._authentication_schemes

    @authentication_schemes.setter
    def authentication_schemes(self, authentication_schemes):
        """
        Sets the authentication_schemes of this ScimServiceProviderConfig.
        The list of supported authentication schemes.

        :param authentication_schemes: The authentication_schemes of this ScimServiceProviderConfig.
        :type: list[ScimServiceProviderConfigAuthenticationScheme]
        """
        
        self._authentication_schemes = authentication_schemes

    @property
    def meta(self):
        """
        Gets the meta of this ScimServiceProviderConfig.
        The metadata of the SCIM resource.

        :return: The meta of this ScimServiceProviderConfig.
        :rtype: ScimMetadata
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this ScimServiceProviderConfig.
        The metadata of the SCIM resource.

        :param meta: The meta of this ScimServiceProviderConfig.
        :type: ScimMetadata
        """
        
        self._meta = meta

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

