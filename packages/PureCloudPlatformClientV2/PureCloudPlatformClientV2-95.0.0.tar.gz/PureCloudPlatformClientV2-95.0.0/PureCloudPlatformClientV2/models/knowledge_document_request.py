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

class KnowledgeDocumentRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        KnowledgeDocumentRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'external_url': 'str',
            'faq': 'DocumentFaq',
            'categories': 'list[DocumentCategoryInput]'
        }

        self.attribute_map = {
            'type': 'type',
            'external_url': 'externalUrl',
            'faq': 'faq',
            'categories': 'categories'
        }

        self._type = None
        self._external_url = None
        self._faq = None
        self._categories = None

    @property
    def type(self):
        """
        Gets the type of this KnowledgeDocumentRequest.
        Document type according to assigned template

        :return: The type of this KnowledgeDocumentRequest.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this KnowledgeDocumentRequest.
        Document type according to assigned template

        :param type: The type of this KnowledgeDocumentRequest.
        :type: str
        """
        allowed_values = ["Faq"]
        if type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for type -> " + type
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def external_url(self):
        """
        Gets the external_url of this KnowledgeDocumentRequest.
        External Url to the document

        :return: The external_url of this KnowledgeDocumentRequest.
        :rtype: str
        """
        return self._external_url

    @external_url.setter
    def external_url(self, external_url):
        """
        Sets the external_url of this KnowledgeDocumentRequest.
        External Url to the document

        :param external_url: The external_url of this KnowledgeDocumentRequest.
        :type: str
        """
        
        self._external_url = external_url

    @property
    def faq(self):
        """
        Gets the faq of this KnowledgeDocumentRequest.
        Faq document details

        :return: The faq of this KnowledgeDocumentRequest.
        :rtype: DocumentFaq
        """
        return self._faq

    @faq.setter
    def faq(self, faq):
        """
        Sets the faq of this KnowledgeDocumentRequest.
        Faq document details

        :param faq: The faq of this KnowledgeDocumentRequest.
        :type: DocumentFaq
        """
        
        self._faq = faq

    @property
    def categories(self):
        """
        Gets the categories of this KnowledgeDocumentRequest.
        Document categories

        :return: The categories of this KnowledgeDocumentRequest.
        :rtype: list[DocumentCategoryInput]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """
        Sets the categories of this KnowledgeDocumentRequest.
        Document categories

        :param categories: The categories of this KnowledgeDocumentRequest.
        :type: list[DocumentCategoryInput]
        """
        
        self._categories = categories

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

