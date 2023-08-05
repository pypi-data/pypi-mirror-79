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

class BuManagementUnitScheduleSummary(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuManagementUnitScheduleSummary - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'management_unit': 'ManagementUnitReference',
            'agent_count': 'int',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'agents': 'list[UserReference]'
        }

        self.attribute_map = {
            'management_unit': 'managementUnit',
            'agent_count': 'agentCount',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'agents': 'agents'
        }

        self._management_unit = None
        self._agent_count = None
        self._start_date = None
        self._end_date = None
        self._agents = None

    @property
    def management_unit(self):
        """
        Gets the management_unit of this BuManagementUnitScheduleSummary.
        The management unit to which this summary applies

        :return: The management_unit of this BuManagementUnitScheduleSummary.
        :rtype: ManagementUnitReference
        """
        return self._management_unit

    @management_unit.setter
    def management_unit(self, management_unit):
        """
        Sets the management_unit of this BuManagementUnitScheduleSummary.
        The management unit to which this summary applies

        :param management_unit: The management_unit of this BuManagementUnitScheduleSummary.
        :type: ManagementUnitReference
        """
        
        self._management_unit = management_unit

    @property
    def agent_count(self):
        """
        Gets the agent_count of this BuManagementUnitScheduleSummary.
        The number of agents from this management unit that are in the schedule

        :return: The agent_count of this BuManagementUnitScheduleSummary.
        :rtype: int
        """
        return self._agent_count

    @agent_count.setter
    def agent_count(self, agent_count):
        """
        Sets the agent_count of this BuManagementUnitScheduleSummary.
        The number of agents from this management unit that are in the schedule

        :param agent_count: The agent_count of this BuManagementUnitScheduleSummary.
        :type: int
        """
        
        self._agent_count = agent_count

    @property
    def start_date(self):
        """
        Gets the start_date of this BuManagementUnitScheduleSummary.
        The start of the schedule change in the management unit. Only populated in schedule update notifications. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_date of this BuManagementUnitScheduleSummary.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this BuManagementUnitScheduleSummary.
        The start of the schedule change in the management unit. Only populated in schedule update notifications. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_date: The start_date of this BuManagementUnitScheduleSummary.
        :type: datetime
        """
        
        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this BuManagementUnitScheduleSummary.
        The end of the schedule change in the management unit. Only populated in schedule update notifications. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The end_date of this BuManagementUnitScheduleSummary.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this BuManagementUnitScheduleSummary.
        The end of the schedule change in the management unit. Only populated in schedule update notifications. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param end_date: The end_date of this BuManagementUnitScheduleSummary.
        :type: datetime
        """
        
        self._end_date = end_date

    @property
    def agents(self):
        """
        Gets the agents of this BuManagementUnitScheduleSummary.
        The changed agents in the management unit. Only populated in schedule update notifications

        :return: The agents of this BuManagementUnitScheduleSummary.
        :rtype: list[UserReference]
        """
        return self._agents

    @agents.setter
    def agents(self, agents):
        """
        Sets the agents of this BuManagementUnitScheduleSummary.
        The changed agents in the management unit. Only populated in schedule update notifications

        :param agents: The agents of this BuManagementUnitScheduleSummary.
        :type: list[UserReference]
        """
        
        self._agents = agents

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

