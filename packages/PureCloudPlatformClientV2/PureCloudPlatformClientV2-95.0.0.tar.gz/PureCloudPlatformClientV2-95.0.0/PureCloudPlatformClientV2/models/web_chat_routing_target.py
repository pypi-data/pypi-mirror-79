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

class WebChatRoutingTarget(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebChatRoutingTarget - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'target_type': 'str',
            'target_address': 'str',
            'skills': 'list[str]',
            'language': 'str',
            'priority': 'int'
        }

        self.attribute_map = {
            'target_type': 'targetType',
            'target_address': 'targetAddress',
            'skills': 'skills',
            'language': 'language',
            'priority': 'priority'
        }

        self._target_type = None
        self._target_address = None
        self._skills = None
        self._language = None
        self._priority = None

    @property
    def target_type(self):
        """
        Gets the target_type of this WebChatRoutingTarget.
        The target type of the routing target, such as 'QUEUE'.

        :return: The target_type of this WebChatRoutingTarget.
        :rtype: str
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """
        Sets the target_type of this WebChatRoutingTarget.
        The target type of the routing target, such as 'QUEUE'.

        :param target_type: The target_type of this WebChatRoutingTarget.
        :type: str
        """
        allowed_values = ["QUEUE"]
        if target_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for target_type -> " + target_type
            self._target_type = "outdated_sdk_version"
        else:
            self._target_type = target_type

    @property
    def target_address(self):
        """
        Gets the target_address of this WebChatRoutingTarget.
        The target of the route, in the format appropriate given the 'targetType'.

        :return: The target_address of this WebChatRoutingTarget.
        :rtype: str
        """
        return self._target_address

    @target_address.setter
    def target_address(self, target_address):
        """
        Sets the target_address of this WebChatRoutingTarget.
        The target of the route, in the format appropriate given the 'targetType'.

        :param target_address: The target_address of this WebChatRoutingTarget.
        :type: str
        """
        
        self._target_address = target_address

    @property
    def skills(self):
        """
        Gets the skills of this WebChatRoutingTarget.
        The list of skill names to use for routing.

        :return: The skills of this WebChatRoutingTarget.
        :rtype: list[str]
        """
        return self._skills

    @skills.setter
    def skills(self, skills):
        """
        Sets the skills of this WebChatRoutingTarget.
        The list of skill names to use for routing.

        :param skills: The skills of this WebChatRoutingTarget.
        :type: list[str]
        """
        
        self._skills = skills

    @property
    def language(self):
        """
        Gets the language of this WebChatRoutingTarget.
        The language name to use for routing.

        :return: The language of this WebChatRoutingTarget.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """
        Sets the language of this WebChatRoutingTarget.
        The language name to use for routing.

        :param language: The language of this WebChatRoutingTarget.
        :type: str
        """
        
        self._language = language

    @property
    def priority(self):
        """
        Gets the priority of this WebChatRoutingTarget.
        The priority to assign to the conversation for routing.

        :return: The priority of this WebChatRoutingTarget.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this WebChatRoutingTarget.
        The priority to assign to the conversation for routing.

        :param priority: The priority of this WebChatRoutingTarget.
        :type: int
        """
        
        self._priority = priority

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

