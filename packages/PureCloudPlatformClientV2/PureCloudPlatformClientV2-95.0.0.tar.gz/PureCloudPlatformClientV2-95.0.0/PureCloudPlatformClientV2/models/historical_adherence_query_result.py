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

class HistoricalAdherenceQueryResult(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        HistoricalAdherenceQueryResult - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user_id': 'str',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'adherence_percentage': 'float',
            'conformance_percentage': 'float',
            'impact': 'str',
            'exception_info': 'list[HistoricalAdherenceExceptionInfo]',
            'day_metrics': 'list[HistoricalAdherenceDayMetrics]',
            'actuals': 'list[HistoricalAdherenceActuals]'
        }

        self.attribute_map = {
            'user_id': 'userId',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'adherence_percentage': 'adherencePercentage',
            'conformance_percentage': 'conformancePercentage',
            'impact': 'impact',
            'exception_info': 'exceptionInfo',
            'day_metrics': 'dayMetrics',
            'actuals': 'actuals'
        }

        self._user_id = None
        self._start_date = None
        self._end_date = None
        self._adherence_percentage = None
        self._conformance_percentage = None
        self._impact = None
        self._exception_info = None
        self._day_metrics = None
        self._actuals = None

    @property
    def user_id(self):
        """
        Gets the user_id of this HistoricalAdherenceQueryResult.
        The ID of the user for whom the adherence is queried

        :return: The user_id of this HistoricalAdherenceQueryResult.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this HistoricalAdherenceQueryResult.
        The ID of the user for whom the adherence is queried

        :param user_id: The user_id of this HistoricalAdherenceQueryResult.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def start_date(self):
        """
        Gets the start_date of this HistoricalAdherenceQueryResult.
        Beginning of the date range that was queried, in ISO-8601 format

        :return: The start_date of this HistoricalAdherenceQueryResult.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this HistoricalAdherenceQueryResult.
        Beginning of the date range that was queried, in ISO-8601 format

        :param start_date: The start_date of this HistoricalAdherenceQueryResult.
        :type: datetime
        """
        
        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this HistoricalAdherenceQueryResult.
        End of the date range that was queried, in ISO-8601 format. If it was not set, end date will be set to the queried time

        :return: The end_date of this HistoricalAdherenceQueryResult.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this HistoricalAdherenceQueryResult.
        End of the date range that was queried, in ISO-8601 format. If it was not set, end date will be set to the queried time

        :param end_date: The end_date of this HistoricalAdherenceQueryResult.
        :type: datetime
        """
        
        self._end_date = end_date

    @property
    def adherence_percentage(self):
        """
        Gets the adherence_percentage of this HistoricalAdherenceQueryResult.
        Adherence percentage for this user, in the scale of 0 - 100

        :return: The adherence_percentage of this HistoricalAdherenceQueryResult.
        :rtype: float
        """
        return self._adherence_percentage

    @adherence_percentage.setter
    def adherence_percentage(self, adherence_percentage):
        """
        Sets the adherence_percentage of this HistoricalAdherenceQueryResult.
        Adherence percentage for this user, in the scale of 0 - 100

        :param adherence_percentage: The adherence_percentage of this HistoricalAdherenceQueryResult.
        :type: float
        """
        
        self._adherence_percentage = adherence_percentage

    @property
    def conformance_percentage(self):
        """
        Gets the conformance_percentage of this HistoricalAdherenceQueryResult.
        Conformance percentage for this user, in the scale of 0 - 100. Conformance percentage can be greater than 100 when the actual on queue time is greater than the scheduled on queue time for the same period.

        :return: The conformance_percentage of this HistoricalAdherenceQueryResult.
        :rtype: float
        """
        return self._conformance_percentage

    @conformance_percentage.setter
    def conformance_percentage(self, conformance_percentage):
        """
        Sets the conformance_percentage of this HistoricalAdherenceQueryResult.
        Conformance percentage for this user, in the scale of 0 - 100. Conformance percentage can be greater than 100 when the actual on queue time is greater than the scheduled on queue time for the same period.

        :param conformance_percentage: The conformance_percentage of this HistoricalAdherenceQueryResult.
        :type: float
        """
        
        self._conformance_percentage = conformance_percentage

    @property
    def impact(self):
        """
        Gets the impact of this HistoricalAdherenceQueryResult.
        The impact of the current adherence state for this user

        :return: The impact of this HistoricalAdherenceQueryResult.
        :rtype: str
        """
        return self._impact

    @impact.setter
    def impact(self, impact):
        """
        Sets the impact of this HistoricalAdherenceQueryResult.
        The impact of the current adherence state for this user

        :param impact: The impact of this HistoricalAdherenceQueryResult.
        :type: str
        """
        allowed_values = ["Positive", "Negative", "Neutral", "Unknown"]
        if impact.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for impact -> " + impact
            self._impact = "outdated_sdk_version"
        else:
            self._impact = impact

    @property
    def exception_info(self):
        """
        Gets the exception_info of this HistoricalAdherenceQueryResult.
        List of adherence exceptions for this user

        :return: The exception_info of this HistoricalAdherenceQueryResult.
        :rtype: list[HistoricalAdherenceExceptionInfo]
        """
        return self._exception_info

    @exception_info.setter
    def exception_info(self, exception_info):
        """
        Sets the exception_info of this HistoricalAdherenceQueryResult.
        List of adherence exceptions for this user

        :param exception_info: The exception_info of this HistoricalAdherenceQueryResult.
        :type: list[HistoricalAdherenceExceptionInfo]
        """
        
        self._exception_info = exception_info

    @property
    def day_metrics(self):
        """
        Gets the day_metrics of this HistoricalAdherenceQueryResult.
        Adherence and conformance metrics for days in query range

        :return: The day_metrics of this HistoricalAdherenceQueryResult.
        :rtype: list[HistoricalAdherenceDayMetrics]
        """
        return self._day_metrics

    @day_metrics.setter
    def day_metrics(self, day_metrics):
        """
        Sets the day_metrics of this HistoricalAdherenceQueryResult.
        Adherence and conformance metrics for days in query range

        :param day_metrics: The day_metrics of this HistoricalAdherenceQueryResult.
        :type: list[HistoricalAdherenceDayMetrics]
        """
        
        self._day_metrics = day_metrics

    @property
    def actuals(self):
        """
        Gets the actuals of this HistoricalAdherenceQueryResult.
        List of actual activity with offset for this user

        :return: The actuals of this HistoricalAdherenceQueryResult.
        :rtype: list[HistoricalAdherenceActuals]
        """
        return self._actuals

    @actuals.setter
    def actuals(self, actuals):
        """
        Sets the actuals of this HistoricalAdherenceQueryResult.
        List of actual activity with offset for this user

        :param actuals: The actuals of this HistoricalAdherenceQueryResult.
        :type: list[HistoricalAdherenceActuals]
        """
        
        self._actuals = actuals

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

