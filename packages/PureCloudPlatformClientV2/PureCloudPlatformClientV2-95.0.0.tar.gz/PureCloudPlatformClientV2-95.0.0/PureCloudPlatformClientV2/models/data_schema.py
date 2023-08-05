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

class DataSchema(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DataSchema - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'version': 'int',
            'applies_to': 'list[str]',
            'enabled': 'bool',
            'created_by': 'DomainEntityRef',
            'date_created': 'datetime',
            'json_schema': 'JsonSchemaDocument',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'applies_to': 'appliesTo',
            'enabled': 'enabled',
            'created_by': 'createdBy',
            'date_created': 'dateCreated',
            'json_schema': 'jsonSchema',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._version = None
        self._applies_to = None
        self._enabled = None
        self._created_by = None
        self._date_created = None
        self._json_schema = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this DataSchema.
        The globally unique identifier for the object.

        :return: The id of this DataSchema.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DataSchema.
        The globally unique identifier for the object.

        :param id: The id of this DataSchema.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DataSchema.


        :return: The name of this DataSchema.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DataSchema.


        :param name: The name of this DataSchema.
        :type: str
        """
        
        self._name = name

    @property
    def version(self):
        """
        Gets the version of this DataSchema.
        The schema's version, a positive integer. Required for updates.

        :return: The version of this DataSchema.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DataSchema.
        The schema's version, a positive integer. Required for updates.

        :param version: The version of this DataSchema.
        :type: int
        """
        
        self._version = version

    @property
    def applies_to(self):
        """
        Gets the applies_to of this DataSchema.
        One of \"CONTACT\" or \"EXTERNAL_ORGANIZATION\".  Indicates the built-in entity type to which this schema applies.

        :return: The applies_to of this DataSchema.
        :rtype: list[str]
        """
        return self._applies_to

    @applies_to.setter
    def applies_to(self, applies_to):
        """
        Sets the applies_to of this DataSchema.
        One of \"CONTACT\" or \"EXTERNAL_ORGANIZATION\".  Indicates the built-in entity type to which this schema applies.

        :param applies_to: The applies_to of this DataSchema.
        :type: list[str]
        """
        
        self._applies_to = applies_to

    @property
    def enabled(self):
        """
        Gets the enabled of this DataSchema.
        The schema's enabled/disabled status. A disabled schema cannot be assigned to any other entities, but the data on those entities from the schema still exists.

        :return: The enabled of this DataSchema.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this DataSchema.
        The schema's enabled/disabled status. A disabled schema cannot be assigned to any other entities, but the data on those entities from the schema still exists.

        :param enabled: The enabled of this DataSchema.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def created_by(self):
        """
        Gets the created_by of this DataSchema.
        The URI of the user that created this schema.

        :return: The created_by of this DataSchema.
        :rtype: DomainEntityRef
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this DataSchema.
        The URI of the user that created this schema.

        :param created_by: The created_by of this DataSchema.
        :type: DomainEntityRef
        """
        
        self._created_by = created_by

    @property
    def date_created(self):
        """
        Gets the date_created of this DataSchema.
        The date and time this schema was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this DataSchema.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this DataSchema.
        The date and time this schema was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this DataSchema.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def json_schema(self):
        """
        Gets the json_schema of this DataSchema.
        A JSON schema defining the extension to the built-in entity type.

        :return: The json_schema of this DataSchema.
        :rtype: JsonSchemaDocument
        """
        return self._json_schema

    @json_schema.setter
    def json_schema(self, json_schema):
        """
        Sets the json_schema of this DataSchema.
        A JSON schema defining the extension to the built-in entity type.

        :param json_schema: The json_schema of this DataSchema.
        :type: JsonSchemaDocument
        """
        
        self._json_schema = json_schema

    @property
    def self_uri(self):
        """
        Gets the self_uri of this DataSchema.
        The URI for this object

        :return: The self_uri of this DataSchema.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this DataSchema.
        The URI for this object

        :param self_uri: The self_uri of this DataSchema.
        :type: str
        """
        
        self._self_uri = self_uri

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

