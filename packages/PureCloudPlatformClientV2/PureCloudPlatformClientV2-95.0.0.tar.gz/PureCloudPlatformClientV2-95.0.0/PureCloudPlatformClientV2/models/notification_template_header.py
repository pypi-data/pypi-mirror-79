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

class NotificationTemplateHeader(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        NotificationTemplateHeader - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'text': 'str',
            'media': 'ContentAttachment',
            'parameters': 'list[NotificationTemplateParameter]'
        }

        self.attribute_map = {
            'type': 'type',
            'text': 'text',
            'media': 'media',
            'parameters': 'parameters'
        }

        self._type = None
        self._text = None
        self._media = None
        self._parameters = None

    @property
    def type(self):
        """
        Gets the type of this NotificationTemplateHeader.
        Template header type

        :return: The type of this NotificationTemplateHeader.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this NotificationTemplateHeader.
        Template header type

        :param type: The type of this NotificationTemplateHeader.
        :type: str
        """
        allowed_values = ["Text", "Media"]
        if type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for type -> " + type
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def text(self):
        """
        Gets the text of this NotificationTemplateHeader.
        Header text. For WhatsApp, ignored

        :return: The text of this NotificationTemplateHeader.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this NotificationTemplateHeader.
        Header text. For WhatsApp, ignored

        :param text: The text of this NotificationTemplateHeader.
        :type: str
        """
        
        self._text = text

    @property
    def media(self):
        """
        Gets the media of this NotificationTemplateHeader.
        Attachment object

        :return: The media of this NotificationTemplateHeader.
        :rtype: ContentAttachment
        """
        return self._media

    @media.setter
    def media(self, media):
        """
        Sets the media of this NotificationTemplateHeader.
        Attachment object

        :param media: The media of this NotificationTemplateHeader.
        :type: ContentAttachment
        """
        
        self._media = media

    @property
    def parameters(self):
        """
        Gets the parameters of this NotificationTemplateHeader.
        Template parameters for placeholders in template

        :return: The parameters of this NotificationTemplateHeader.
        :rtype: list[NotificationTemplateParameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this NotificationTemplateHeader.
        Template parameters for placeholders in template

        :param parameters: The parameters of this NotificationTemplateHeader.
        :type: list[NotificationTemplateParameter]
        """
        
        self._parameters = parameters

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

