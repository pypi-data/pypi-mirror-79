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

class AuthzGrantPolicy(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AuthzGrantPolicy - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'actions': 'list[str]',
            'condition': 'str',
            'domain': 'str',
            'entity_name': 'str'
        }

        self.attribute_map = {
            'actions': 'actions',
            'condition': 'condition',
            'domain': 'domain',
            'entity_name': 'entityName'
        }

        self._actions = None
        self._condition = None
        self._domain = None
        self._entity_name = None

    @property
    def actions(self):
        """
        Gets the actions of this AuthzGrantPolicy.


        :return: The actions of this AuthzGrantPolicy.
        :rtype: list[str]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this AuthzGrantPolicy.


        :param actions: The actions of this AuthzGrantPolicy.
        :type: list[str]
        """
        
        self._actions = actions

    @property
    def condition(self):
        """
        Gets the condition of this AuthzGrantPolicy.


        :return: The condition of this AuthzGrantPolicy.
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this AuthzGrantPolicy.


        :param condition: The condition of this AuthzGrantPolicy.
        :type: str
        """
        
        self._condition = condition

    @property
    def domain(self):
        """
        Gets the domain of this AuthzGrantPolicy.


        :return: The domain of this AuthzGrantPolicy.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """
        Sets the domain of this AuthzGrantPolicy.


        :param domain: The domain of this AuthzGrantPolicy.
        :type: str
        """
        
        self._domain = domain

    @property
    def entity_name(self):
        """
        Gets the entity_name of this AuthzGrantPolicy.


        :return: The entity_name of this AuthzGrantPolicy.
        :rtype: str
        """
        return self._entity_name

    @entity_name.setter
    def entity_name(self, entity_name):
        """
        Sets the entity_name of this AuthzGrantPolicy.


        :param entity_name: The entity_name of this AuthzGrantPolicy.
        :type: str
        """
        
        self._entity_name = entity_name

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

