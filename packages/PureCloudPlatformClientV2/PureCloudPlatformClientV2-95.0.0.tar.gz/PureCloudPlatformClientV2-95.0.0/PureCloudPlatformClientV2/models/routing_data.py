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

class RoutingData(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RoutingData - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'queue_id': 'str',
            'language_id': 'str',
            'priority': 'int',
            'skill_ids': 'list[str]',
            'preferred_agent_ids': 'list[str]'
        }

        self.attribute_map = {
            'queue_id': 'queueId',
            'language_id': 'languageId',
            'priority': 'priority',
            'skill_ids': 'skillIds',
            'preferred_agent_ids': 'preferredAgentIds'
        }

        self._queue_id = None
        self._language_id = None
        self._priority = None
        self._skill_ids = None
        self._preferred_agent_ids = None

    @property
    def queue_id(self):
        """
        Gets the queue_id of this RoutingData.
        The identifier of the routing queue

        :return: The queue_id of this RoutingData.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """
        Sets the queue_id of this RoutingData.
        The identifier of the routing queue

        :param queue_id: The queue_id of this RoutingData.
        :type: str
        """
        
        self._queue_id = queue_id

    @property
    def language_id(self):
        """
        Gets the language_id of this RoutingData.
        The identifier of a language to be considered in routing

        :return: The language_id of this RoutingData.
        :rtype: str
        """
        return self._language_id

    @language_id.setter
    def language_id(self, language_id):
        """
        Sets the language_id of this RoutingData.
        The identifier of a language to be considered in routing

        :param language_id: The language_id of this RoutingData.
        :type: str
        """
        
        self._language_id = language_id

    @property
    def priority(self):
        """
        Gets the priority of this RoutingData.
        The priority for routing

        :return: The priority of this RoutingData.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this RoutingData.
        The priority for routing

        :param priority: The priority of this RoutingData.
        :type: int
        """
        
        self._priority = priority

    @property
    def skill_ids(self):
        """
        Gets the skill_ids of this RoutingData.
        A list of skill identifiers to be considered in routing

        :return: The skill_ids of this RoutingData.
        :rtype: list[str]
        """
        return self._skill_ids

    @skill_ids.setter
    def skill_ids(self, skill_ids):
        """
        Sets the skill_ids of this RoutingData.
        A list of skill identifiers to be considered in routing

        :param skill_ids: The skill_ids of this RoutingData.
        :type: list[str]
        """
        
        self._skill_ids = skill_ids

    @property
    def preferred_agent_ids(self):
        """
        Gets the preferred_agent_ids of this RoutingData.
        A list of agents to be preferred in routing

        :return: The preferred_agent_ids of this RoutingData.
        :rtype: list[str]
        """
        return self._preferred_agent_ids

    @preferred_agent_ids.setter
    def preferred_agent_ids(self, preferred_agent_ids):
        """
        Sets the preferred_agent_ids of this RoutingData.
        A list of agents to be preferred in routing

        :param preferred_agent_ids: The preferred_agent_ids of this RoutingData.
        :type: list[str]
        """
        
        self._preferred_agent_ids = preferred_agent_ids

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

