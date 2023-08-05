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

class DocumentUpload(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DocumentUpload - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'workspace': 'DomainEntityRef',
            'tags': 'list[str]',
            'tag_ids': 'list[str]'
        }

        self.attribute_map = {
            'name': 'name',
            'workspace': 'workspace',
            'tags': 'tags',
            'tag_ids': 'tagIds'
        }

        self._name = None
        self._workspace = None
        self._tags = None
        self._tag_ids = None

    @property
    def name(self):
        """
        Gets the name of this DocumentUpload.
        The name of the document

        :return: The name of this DocumentUpload.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DocumentUpload.
        The name of the document

        :param name: The name of this DocumentUpload.
        :type: str
        """
        
        self._name = name

    @property
    def workspace(self):
        """
        Gets the workspace of this DocumentUpload.
        The workspace the document will be uploaded to

        :return: The workspace of this DocumentUpload.
        :rtype: DomainEntityRef
        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace):
        """
        Sets the workspace of this DocumentUpload.
        The workspace the document will be uploaded to

        :param workspace: The workspace of this DocumentUpload.
        :type: DomainEntityRef
        """
        
        self._workspace = workspace

    @property
    def tags(self):
        """
        Gets the tags of this DocumentUpload.


        :return: The tags of this DocumentUpload.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this DocumentUpload.


        :param tags: The tags of this DocumentUpload.
        :type: list[str]
        """
        
        self._tags = tags

    @property
    def tag_ids(self):
        """
        Gets the tag_ids of this DocumentUpload.


        :return: The tag_ids of this DocumentUpload.
        :rtype: list[str]
        """
        return self._tag_ids

    @tag_ids.setter
    def tag_ids(self, tag_ids):
        """
        Sets the tag_ids of this DocumentUpload.


        :param tag_ids: The tag_ids of this DocumentUpload.
        :type: list[str]
        """
        
        self._tag_ids = tag_ids

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

